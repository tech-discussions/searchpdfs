import os
from flask import Flask, request, redirect, url_for, flash, render_template_string
from werkzeug.utils import secure_filename
from tika import parser
import pysolr

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'pdf'}
SOLR_URL = 'http://solr:8983/solr/search_pdf'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            index_in_solr(filename, extract_text_tika(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))
    return upload_form()


@app.route('/search', methods=['GET'])
def search_solr():
    results = []
    query = request.args.get('query', None)
    search_option = request.args.get('search_option', 'filename')
    if query is not None:
        field = 'id' if search_option == 'filename' else 'content'
        solr = pysolr.Solr(SOLR_URL, timeout=10)
        results = solr.search(f"{field}:(*{query}*)")
        return search_form(results, query, search_option)
    

def search_form(results, query, search_option):
    return render_template_string('''
    <!doctype html>
    <title>Search Solr</title>
    <h1>Search Solr</h1>
    <form method=get>
      <input type=text name=query placeholder="Enter search query" {% if query %}value="{{ query }}"{% endif %} required>
      <br>
      <label>
        <input type=radio name=search_option value=filename {% if search_option == 'filename' %}checked{% endif %}> Filename
      </label>
      <label>
        <input type=radio name=search_option value=content {% if search_option == 'content' %}checked{% endif %}> Content
      </label>
      <br>
      <input type=submit value=Search>
    </form>
    {% if results %}
      <h2>Search Results:</h2>
      <ul>
        {% for result in results %}
          <li>{{ result['id'] }}</li>
        {% endfor %}
      </ul>
    {% endif %}
    ''', results=results, query=query, search_option=search_option)    

def upload_form():
    return '''
    <!doctype html>
    <title>Upload PDF File</title>
    <h1>Upload PDF File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def extract_text_tika(file_path):
    parsed_pdf = parser.from_file(file_path)
    pdf_text = parsed_pdf['content']
    return pdf_text.strip()


def index_in_solr(pdf_filename, pdf_text):
    solr = pysolr.Solr(SOLR_URL, timeout=10)
    solr.add([{'id': pdf_filename, 'content': pdf_text}])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

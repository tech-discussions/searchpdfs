"""
A Flask web application for uploading, indexing, and searching PDF files in Solr.

The application provides a file upload form for uploading PDF files. The uploaded files are saved
to a local directory and their text content is extracted using Apache Tika. The file names and
extracted text are then indexed in Solr.

The application also provides a search form for searching Solr based on file name or text content.
"""

import os
from flask import Flask, request, redirect, url_for, flash, render_template_string
from werkzeug.utils import secure_filename
from tika import parser
import pysolr

# Import variables from config.py
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, SOLR_URL


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Handle file upload and indexing in Solr.

    If the request method is POST, process the uploaded file, save it, 
    and index its content in Solr. Otherwise, return the upload form.
    """

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
            index_in_solr(filename, extract_text_tika(
                os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))
    return upload_form()


@app.route('/search', methods=['GET'])
def search_solr():
    """
    Search for documents in Solr based on the user's query and search option (filename or content).

    :return: A rendered HTML template with the search form and results (if any).
    """
    results = []
    query = request.args.get('query', None)
    search_option = request.args.get('search_option', 'filename')
    if query is not None:
        field = 'id' if search_option == 'filename' else 'content'
        solr = pysolr.Solr(SOLR_URL, timeout=10)
        results = solr.search(f"{field}:(*{query}*)")
    return search_form(results, query, search_option)


def search_form(results, query, search_option):
    """
    Render the search form with results, if any.

    :param results: The search results to display.
    :param query: The search query entered by the user.
    :param search_option: The search option selected by the user (filename or content).
    :return: A rendered HTML template with the search form and results.
    """
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
    """
    Render the file upload form.

    :return: A rendered HTML template with the file upload form.
    """

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
    """
    Extract text from a PDF file using Apache Tika.

    :param file_path: The path to the PDF file to extract text from.
    :return: The extracted text.
    """

    parsed_pdf = parser.from_file(file_path)
    pdf_text = parsed_pdf['content']
    return pdf_text.strip()


def index_in_solr(pdf_filename, pdf_text):
    """
    Index a PDF file and its extracted text in Solr.

    :param pdf_filename: The name of the PDF file to index.
    :param pdf_text: The extracted text from the PDF file.
    """

    solr = pysolr.Solr(SOLR_URL, timeout=10)
    solr.add([{'id': pdf_filename, 'content': pdf_text}])


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    :param filename: The name of the file to check.
    :return: True if the file has an allowed extension, False otherwise.
    """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

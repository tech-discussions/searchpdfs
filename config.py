"""
Configuration variables for the Flask web application.

This module contains configuration variables such as the upload folder, allowed file extensions, 
and Solr URL. These variables are imported and used by the main Flask application (app.py).
"""

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'pdf'}
SOLR_URL = 'http://solr:8983/solr/search_pdf'

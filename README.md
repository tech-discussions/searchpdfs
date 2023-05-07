# PDF Indexing and Searching with Solr

This project demonstrates how to index PDF files and search their contents using Apache Solr, Tika, and Flask.

## Overview

The application consists of two main components:

1. A Flask web server that handles file uploads and search queries.
2. Apache Solr, which indexes and searches the PDF files.

The application allows users to:

- Upload PDF files to the server.
- Index the PDF files by their filename and content.
- Search for PDF files by filename or content.

## Dependencies

The following libraries and tools are used in this project:

- Flask: A lightweight web framework for Python.
- Werkzeug: A library for handling secure file uploads.
- Tika: A Python library for extracting text from PDF files.
- PySolr: A Python library for interacting with Apache Solr.

## Project Structure

```
.
├── app.py                  # Flask application
├── Dockerfile              # Dockerfile for building the Flask application container
├── docker-compose.yml      # Docker Compose configuration for running the entire project
├── requirements.txt        # Python dependencies
└── UPLOAD_FOLDER           # Folder for storing uploaded PDF files
```

## Installation and Setup

1. Install Docker and Docker Compose on your machine if you haven't already.
2. Clone the project repository.
3. Navigate to the project directory.
4. Run `docker-compose up --build` to build the Docker images and start the containers.

## Usage

1. Access the Flask application at `http://localhost:8000`.
2. Use the `/upload` endpoint to upload PDF files.
3. Use the `/search` endpoint to search for PDF files by filename or content.

## API Endpoints

### `/upload` (GET, POST)

This endpoint displays an HTML form to upload a PDF file. When a file is submitted, it is saved to the `UPLOAD_FOLDER`, and its text content is extracted using Tika. The file is then indexed in Solr by its filename and content.

### `/search` (GET)

This endpoint displays an HTML form to search for PDF files by filename or content. When a search query is submitted, the application queries Solr and returns a list of matching files.

## Configuration

You can configure the following settings in `app.py`:

- `UPLOAD_FOLDER`: The path to the folder where uploaded PDF files are stored. Defaults to `./`.
- `ALLOWED_EXTENSIONS`: A set of allowed file extensions for uploads. Defaults to `{'pdf'}`.
- `SOLR_URL`: The URL to the Solr server. Defaults to `http://solr:8983/solr/search_pdf`.

## Known Issues

- Tika may not always be able to extract text from certain PDF files.
- The Flask application is not designed for production use. For production deployments, consider using a more robust web server like Gunicorn and a reverse proxy like Nginx.
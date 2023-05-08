# PDF Indexing and Searching with Solr

This project demonstrates how to index PDF files and search their contents using Apache Solr, Tika, and Flask.

## Motivation

In today's world, we are surrounded by data in various formats like text, audio, images, and videos. Text data is one of the most abundant and valuable sources of information. With the increase in the use of PDFs, it becomes challenging to extract relevant information from them. This project aims to solve this problem by building a search engine that can extract text content from PDF files, index them, and allow users to search for the desired information. 

The search engine can be useful in various domains like academics, research, legal, and corporate sectors. It can help users save time and effort in searching for information from multiple PDF files. Furthermore, the project can be extended to support other formats like images, audio, and videos, making it a powerful tool for information retrieval.

By using open-source technologies like Flask, Apache Solr, Apache PDFBox, and PyPDF2, the project is accessible to a wide range of users, who can contribute to its development and use it for their specific needs.

## Architecture

    +------------+    +------------+    +------------+
    |            |    |            |    |            |
    |   User     |    |   Flask    |    |   Search   |
    |  Browser   |<-->| Application|<-->|  Interface |
    |            |    |            |    |            |
    +------------+    +-----+------+    +-----+------+
                             |                 |
                             |  HTML / CSS /   |
                             |  JavaScript     |
                             |                 |
                    +--------+--------+--------+-------+
                    |                 |                 |
             +------+    Upload      +------+   Search  +------+
             |      |   PDF Files    |      |   PDFs    |      |
             |      v                 v      |           v      |
             | +-------------+ +-------------+ +-------------+ |
             | |             | |             | |             | |
             | |   Upload    | |    Tika     | |     Solr    | |
             | |   Service   | |   Server    | |   Service   | |
             | |             | |             | |             | |
             | +-------------+ +-------------+ +-------------+ |
             +-------------------+-------------+---------------+
                                 |             |
                        +--------+-------------+-------+
                        |                              |
                  +-----+--------------+     +-------+------------+
                  |    Tika Parser      |     |   Solr Indexer     |
                  |(Extract Text Content|     |(Index Text Content |
                  |     from PDF)       |     |  for Searching)    |
                  +---------------------+     +--------------------+


In this diagram, the user's browser sends requests to the Flask application, which processes the requests and sends responses back to the browser. The Flask application also communicates with the Upload Service, Tika Server, and Solr Service to handle uploading PDF files, extracting text content, and indexing text content for searching. The Tika Parser is responsible for extracting text content from PDF files, and the Solr Indexer is responsible for indexing text content for searching.

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
├── config.py               # Configuration file for the Flask application
├── Dockerfile              # Dockerfile for building the Flask application container
├── docker-compose.yml      # Docker Compose configuration for running the entire project
├── requirements.txt        # Python dependencies
└── UPLOAD_FOLDER           # Folder for storing uploaded PDF files
```

## Installation and Setup(using Docker)

1. Install Docker and Docker Compose on your machine if you haven't already.
2. Clone the project repository.
3. Navigate to the project directory.
4. Run `docker-compose up --build` to build the Docker images and start the containers.
5. Run `docker-compose down` to stop and remove the Docker containers.

## Running the Flask Application Locally (without Docker)

To run the Flask application locally without using Docker, follow these steps:

### Prerequisites

1. Install Python 3 on your machine.
2. Install Apache Solr locally or have access to a remote Solr instance.
3. Install Java Runtime Environment (JRE) for Tika.

### Setup

1. Clone the project repository.
2. Navigate to the project directory.
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - On macOS and Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
5. Install the Python dependencies: `pip install -r requirements.txt`

### Configuration

Update the `SOLR_URL` in `config.py` to point to your local or remote Solr instance.

For example, if your local Solr instance is running on `http://localhost:8983/solr/search_pdf`, update `config.py` as follows:

```python
SOLR_URL = 'http://localhost:8983/solr/search_pdf'
```

### Running the Application

1. In the project directory, start the Flask application: `python app.py`
2. Access the application at `http://localhost:8000`

**Note**: To ensure that the Solr instance is properly set up, you might need to create a collection and configure its schema as demonstrated in the previous sections.

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

You can configure the following settings in `config.py`:

- `UPLOAD_FOLDER`: The path to the folder where uploaded PDF files are stored. Defaults to `./`.
- `ALLOWED_EXTENSIONS`: A set of allowed file extensions for uploads. Defaults to `{'pdf'}`.
- `SOLR_URL`: The URL to the Solr server. Defaults to `http://solr:8983/solr/search_pdf`.

## Known Issues

- Tika may not always be able to extract text from certain PDF files.
- The Flask application is not designed for production use. For production deployments, consider using a more robust web server like Gunicorn and a reverse proxy like Nginx.

## Further Enhancements

Here are some ideas for further enhancements that can be added to the project:

1. **Authentication and authorization**: Implement user authentication and authorization to control access to the application. This can be done using Flask extensions like Flask-Login or Flask-Security.

2. **Pagination**: Implement pagination for search results to improve the user experience and performance when dealing with large result sets.

3. **File management**: Add features for deleting and updating indexed PDF files, as well as reindexing the entire collection.

4. **Richer search features**: Integrate more advanced search features from Solr, such as faceted search, filtering, and sorting.

5. **Support for more file types**: Extend the application to support indexing and searching for other file types, such as Word documents, Excel spreadsheets, and images.

6. **Frontend improvements**: Improve the frontend by using a modern frontend framework like React, Angular, or Vue.js, and style the application with CSS frameworks like Bootstrap or Bulma.

7. **Asynchronous processing**: Use asynchronous processing to handle file uploads and indexing to improve the application's performance and responsiveness, especially when dealing with large files.

8. **Monitoring and logging**: Implement monitoring and logging for the application to track performance and troubleshoot issues. Tools like Sentry, Logstash, and Grafana can be used for this purpose.

9. **Testing**: Write tests for the application using Python testing frameworks like pytest or unittest to ensure the code is working as expected and to prevent regressions.

10. **Container orchestration**: Deploy the application using container orchestration platforms like Kubernetes or Amazon ECS for better scalability and management in production environments.

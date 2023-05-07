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
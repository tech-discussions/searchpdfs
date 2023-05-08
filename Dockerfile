# Use the official Python base image
FROM python:3.11-slim

# Install JRE
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download the required files from Maven Central Repository
RUN wget -O /tmp/tika-server.jar "http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar" && \
    wget -O /tmp/tika-server.jar.md5 "http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar.md5"

# RUN nohup java -jar /tmp/tika-server.jar > output.log 2>&1 &

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Start the application
CMD ["python", "app.py"]

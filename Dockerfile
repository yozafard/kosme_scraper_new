# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy and give execute permission to the install_chrome.sh script
COPY install_chrome.sh /app/install_chrome.sh
RUN chmod +x /app/install_chrome.sh

# Install Chrome and Python dependencies
RUN ./install_chrome.sh

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Set up environment variables for Chrome binary path
ENV PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"
ENV CHROME_BIN="/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

# Clean up unnecessary files
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# Run your Python script
CMD ["python", "./scraper_api.py"]

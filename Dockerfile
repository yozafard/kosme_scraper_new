# Use the official Python image from the Docker Hub
FROM python:3.10-slim

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

# Run your Python script
CMD ["python", "./scraper_api.py"]

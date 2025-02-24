# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies required for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libappindicator3-1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdbus-1-3 \
    libcups2 \
    libxrandr2 \
    libxss1 \
    libgbm-dev \
    libnotify-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Copy and give execute permission to the install_chrome.sh script
COPY install_chrome.sh /app/install_chrome.sh
RUN chmod +x /app/install_chrome.sh

# Install Chrome
RUN ./install_chrome.sh

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Run your Python script
CMD ["python", "./scraper_api.py"]

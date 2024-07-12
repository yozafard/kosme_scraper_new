#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install wget if not already installed
if ! command -v wget &> /dev/null; then
    echo "wget not found, installing..."
    apt-get update
    apt-get install -y wget
fi

# Install dependencies required by Chrome
apt-get update && apt-get install -y \
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
    libnotify-dev

# Download and install Chrome
STORAGE_DIR=/opt/render/project/.render
CHROME_DIR=$STORAGE_DIR/chrome
CHROME_BINARY=$CHROME_DIR/opt/google/chrome/google-chrome

if [[ ! -f $CHROME_BINARY ]]; then
    echo "...Downloading Chrome"
    mkdir -p $CHROME_DIR
    cd $CHROME_DIR
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    dpkg -x google-chrome-stable_current_amd64.deb $CHROME_DIR
    rm google-chrome-stable_current_amd64.deb
else
    echo "...Using Chrome from cache"
fi

# Add Chrome's location to the PATH
ln -s $CHROME_BINARY /usr/bin/google-chrome

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*

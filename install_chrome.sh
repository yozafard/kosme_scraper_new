#!/usr/bin/env bash

# Exit script on any error
set -e

# Update the package list and install dependencies
# apt-get update
# apt-get install -y wget gnupg2

# Install Google Chrome using the downloaded setup file

chmod +x ChromeSetup
./ChromeSetup --install --force --accept-license

# Install Python dependencies
pip install -r requirements.txt

# Optional: Log successful completion
echo "Google Chrome and Python dependencies installation completed successfully."

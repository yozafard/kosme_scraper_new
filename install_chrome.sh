#!/usr/bin/env bash

# Update the package list
apt-get update

# Install dependencies
apt-get install -y wget gnupg2

# Add Google Chrome’s repository
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# Update the package list again to include the new Chrome repository
apt-get update

# Install Google Chrome
apt-get install -y google-chrome-stable

# Install Python dependencies
pip install -r requirements.txt

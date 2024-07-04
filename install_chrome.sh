#!/usr/bin/env bash

# Step 1: Update the package list
apt-get update

# Step 2: Install dependencies
apt-get install -y wget gnupg2

# Step 3: Add Google Chrome’s repository
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# Step 4: Update the package list again to include the new Chrome repository
apt-get update

# Step 5: Install Google Chrome
apt-get install -y google-chrome-stable

# Step 6: Install Python dependencies
pip install -r requirements.txt

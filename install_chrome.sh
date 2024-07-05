#!/usr/bin/env bash
# Exit on error
set -o errexit

# Define storage directory for Chrome
STORAGE_DIR=/opt/render/project/.render

# Check if Chrome is already downloaded
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

# Add Chrome's location to the PATH
# export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"

# Install Python dependencies
pip install -r requirements.txt

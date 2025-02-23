#!/bin/bash

# Script to install all dependencies for the Python script on Linux

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install Chrome
echo "Installing Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
echo "Installing ChromeDriver..."
LATEST_CHROMEDRIVER=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Install system dependencies for Chrome and ChromeDriver
echo "Installing system dependencies..."
sudo apt-get install -y libnss3 libgconf-2-4 libxi6 libgdk-pixbuf2.0-0 libxcomposite1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install requests beautifulsoup4 selenium webdriver-manager flask Flask-HTTPAuth

echo "All dependencies installed successfully!"

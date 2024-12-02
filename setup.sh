#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting setup for macOS..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Install Python3 and MySQL if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    brew install python3
else
    echo "Python3 is already installed."
fi

if ! command -v mysql &> /dev/null; then
    echo "Installing MySQL..."
    brew install mysql
else
    echo "MySQL is already installed."
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Verify pip installation
echo "Installed pip version:"
python3 -m pip --version

# Install Python packages from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "Error: requirements.txt not found in the current directory!"
    exit 1
fi

# Confirm completion
echo "Setup complete! All dependencies have been installed."
#!/bin/bash

# Exit script on any error
set -e

# Function to print messages
print_message() {
    echo -e "\n\033[1;32m$1\033[0m"
}


print_message "Upgrading pip..."
# Upgrade pip in the virtual environment
pip3 install --upgrade pip

print_message "Installing dependencies from requirements.txt..."
# Install the required packages
pip3 install -r requirements.txt

print_message "Running the Flask application..."
# Run the Flask application
print_message "application will be running on port 8000"
print_message "http://localhost:8000"

python3 run_app.py

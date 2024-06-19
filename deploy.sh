#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt file not found!"
fi

# Check if .env file already exists
if [ -f ".env" ]; then
    echo ".env file already exists."
else
    # Create the .env file and add default key-value pairs
    echo "Creating .env file..."
    {
        echo "GOOGLE_API_KEY="
        echo "OPENAI_API_KEY="
    } > .env
    echo ".env file created."
fi

echo "Deployment complete."

#!/bin/bash

# Check if the virtual environment directory exists
if [ -d ".venv" ]; then
    echo "Starting application..."
    source .venv/bin/activate
    python3 -m uvicorn main:app --port 8000 --reload
fi

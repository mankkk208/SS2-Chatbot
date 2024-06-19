@echo off
setlocal enabledelayedexpansion

REM Check if the virtual environment directory exists
IF NOT EXIST ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install the required packages
IF EXIST "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt file not found!
)

REM Check if .env file already exists
IF EXIST ".env" (
    echo .env file already exists.
) ELSE (
    REM Create the .env file and add default key-value pairs
    echo Creating .env file...
    (
        echo GOOGLE_API_KEY=
        echo OPENAI_API_KEY=
    ) > .env
    echo .env file created.
)

echo Deployment complete.

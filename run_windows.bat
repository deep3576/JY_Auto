@echo off
REM Exit on error
setlocal enabledelayedexpansion
set "PYTHON_VERSION=3.12"

REM Function to print messages
call :print_message "Updating system packages..."
REM Ensure `choco` is installed and available for package management
REM Chocolatey installation is assumed to be available in the system

REM Install Python 3.12 if not already installed
call :print_message "Installing Python %PYTHON_VERSION%..."
choco install python --version=%PYTHON_VERSION% -y

REM Ensure pip is up-to-date
call :print_message "Upgrading pip..."
python -m pip install --upgrade pip


REM Install dependencies from requirements.txt
call :print_message "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

REM Run the Flask application
call :print_message "Running the Flask application..."

waitress-serve --host=0.0.0.0 --port=8000 app:app


exit /b

:print_message
echo %~1
exit /b
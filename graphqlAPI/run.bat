@echo off
SETLOCAL

REM Change to the directory where the script is located
cd /d %~dp0

echo ===================================================
echo GraphQL API Launcher
echo ===================================================

REM Check if .venv directory exists
IF NOT EXIST ".venv" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment. Please ensure Python is installed and in your PATH.
        pause
        exit /b %ERRORLEVEL%
    )
    
    echo [INFO] Installing dependencies from requirements.txt...
    .venv\Scripts\pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b %ERRORLEVEL%
    )
    echo [INFO] Setup complete!
) ELSE (
    echo [INFO] Virtual environment found.
)

echo.
echo [INFO] Starting the server...
echo [INFO] GraphQL Playground: http://127.0.0.1:8000/graphql
echo [INFO] REST Products:      http://127.0.0.1:8000/api/v1/productos/
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Run the application using the python executable in the venv
.venv\Scripts\python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

ENDLOCAL

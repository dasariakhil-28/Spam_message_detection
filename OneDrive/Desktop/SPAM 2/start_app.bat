@echo off
REM ============================================================
REM SPAM DETECTION SYSTEM - START SCRIPT (Batch Version)
REM Run this file to start the server and open in browser
REM ============================================================

echo.
echo ==================================================
echo 🚀 SPAM DETECTION SYSTEM STARTUP
echo ==================================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo.

REM Check if model exists
if not exist "spam_model.pkl" (
    echo ⚠️  Warning: Model file not found (spam_model.pkl)
    echo Run: python train_model.py
    echo.
)

echo ==================================================
echo 🌐 Starting Flask Server
echo ==================================================
echo.
echo 📱 Website: http://localhost:5000
echo 🔌 API Endpoint: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

REM Start the Flask app
start cmd /k ".\.venv\Scripts\python.exe app.py"

REM Wait for server to start
timeout /t 3 /nobreak

REM Open in browser
start http://localhost:5000

echo.
echo ✨ SPAM DETECTION SYSTEM IS READY!
echo The server is starting in a new window...
echo.
pause

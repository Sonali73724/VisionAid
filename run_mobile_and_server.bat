@echo off
title VisionAid AI Server and Mobile App
cd /d "%~dp0"
echo ========================================================
echo 1. Starting VisionAid AI Backend Server in a new window...
echo ========================================================
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe!
    pause
    exit /b 1
)

start "VisionAid AI Server" cmd /k ""%~dp0.venv\Scripts\python.exe" "%~dp0server.py""

echo Waiting for AI models to initialize...
ping -n 6 127.0.0.1 >nul

echo ========================================================
echo 2. Starting VisionAid Mobile Client...
echo ========================================================
"%~dp0.venv\Scripts\python.exe" "%~dp0mobile_app.py"
pause

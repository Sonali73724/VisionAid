@echo off
title VisionAid Desktop App
cd /d "%~dp0"
echo ========================================================
echo Starting VisionAid Standalone Desktop Application...
echo ========================================================
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0vision_app.py"
) else (
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe!
    pause
    exit /b 1
)
pause

@echo off
title VisionAid Mobile App
cd /d "%~dp0"
echo Starting VisionAid Mobile Application...
call .venv\Scripts\activate.bat
python mobile_app.py
pause

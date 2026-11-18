@echo off
title VisionAid AI Server
cd /d "%~dp0"
echo Starting VisionAid AI Backend Server on http://127.0.0.1:8000...
call .venv\Scripts\activate.bat
python server.py
pause

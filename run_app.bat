@echo off
title VisionAid Launcher
cd /d "%~dp0"
echo ========================================================
echo               VISIONAID LAUNCHER
echo ========================================================
echo  [1] Standalone Desktop App (Recommended - single window)
echo  [2] Mobile App + Local AI Server (Client-Server)
echo  [3] Exit
echo ========================================================
set /p choice="Enter option (1, 2 or 3) [default: 1]: "

if "%choice%"=="2" goto run_mobile
if "%choice%"=="3" goto end

:run_desktop
call "%~dp0run_desktop_app.bat"
goto end

:run_mobile
call "%~dp0run_mobile_and_server.bat"
goto end

:end

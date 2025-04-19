@echo off
title Cat Companion Launcher
color 0D

:: Change to the script's directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Check if the main script exists
if not exist cat_companion.py (
    echo [ERROR] cat_companion.py not found
    echo Please make sure the script is in the same folder
    pause
    exit /b 1
)

:: Start the application minimized
start /min python cat_companion.py

:: Wait a moment for the application to start
timeout /t 1 /nobreak >nul

:: Exit the batch file
exit 
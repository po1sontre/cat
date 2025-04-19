@echo off
title Cat Companion
color 0D

echo.
echo  /\_/\  
echo ( o.o ) 
echo  > ^< 
echo.
echo Cat Companion
echo ============
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

:: Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyQt6...
    pip install PyQt6
) else (
    echo PyQt6 is already installed
)

:: Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pywin32...
    pip install pywin32
) else (
    echo pywin32 is already installed
)

echo.
echo Starting Cat Companion...
echo.
python cat_companion.py

pause 
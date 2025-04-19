@echo off
title Cat Companion
color 0D
mode con: cols=60 lines=30

:: Clear screen and set cursor position
cls
echo.

:: Print fancy cat logo
echo    /\___/\
echo   (  o o  )
echo   (  =^=  ) ~ Meow!
echo    (______)
echo.

:: Print title with box
echo    ╔══════════════════════════════╗
echo    ║        Cat Companion         ║
echo    ╚══════════════════════════════╝
echo.

:: Print status box
echo    ╔══════════════════════════════╗
echo    ║        Status Check          ║
echo    ╠══════════════════════════════╣

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ❌ Python not found        ║
    echo    ║                            ║
    echo    ║  Please install Python 3.8+ ║
    echo    ║  from python.org           ║
    echo    ╚══════════════════════════════╝
    echo.
    echo    Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    echo    [ERROR] Python is required to run Cat Companion
    echo    Please install Python 3.8 or higher from python.org
    echo    Make sure to check "Add Python to PATH" during installation
    echo.
    echo    Press any key to exit...
    pause >nul
    exit /b 1
) else (
    echo    ║  ✅ Python installed       ║
)

:: Check Python version
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
for /f "tokens=1 delims=." %%I in ("%PYTHON_VERSION%") do set PYTHON_MAJOR=%%I
for /f "tokens=2 delims=." %%I in ("%PYTHON_VERSION%") do set PYTHON_MINOR=%%I

if %PYTHON_MAJOR% LSS 3 (
    echo    ║  ❌ Python version too old  ║
    echo    ║  Need Python 3.8 or higher  ║
    echo    ╚══════════════════════════════╝
    echo.
    echo    Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    echo    [ERROR] Your Python version (%PYTHON_VERSION%) is too old
    echo    Cat Companion requires Python 3.8 or higher
    echo    Please download and install the latest version
    echo.
    echo    Press any key to exit...
    pause >nul
    exit /b 1
) else if %PYTHON_MINOR% LSS 8 (
    echo    ║  ⚠️ Python version old     ║
    echo    ║  Recommend Python 3.8+     ║
) else (
    echo    ║  ✅ Python version OK      ║
)

:: Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ❌ pip not found          ║
    echo    ║  Installing pip...         ║
    python -m ensurepip --default-pip >nul
    if %errorlevel% neq 0 (
        echo    ║  ❌ Failed to install pip  ║
        echo    ╚══════════════════════════════╝
        echo.
        echo    [ERROR] Failed to install pip
        echo    This might be due to:
        echo    1. Python installation is incomplete
        echo    2. No internet connection
        echo    3. Permission issues
        echo.
        echo    Please try:
        echo    1. Reinstalling Python
        echo    2. Running as administrator
        echo    3. Checking your internet connection
        echo.
        echo    Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo    ║  ✅ pip installed          ║
) else (
    echo    ║  ✅ pip installed          ║
)

:: Check internet connection
ping -n 1 python.org >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ❌ No internet connection  ║
    echo    ╚══════════════════════════════╝
    echo.
    echo    [ERROR] No internet connection detected
    echo    Cat Companion needs internet to install required packages
    echo    Please check your connection and try again
    echo.
    echo    Press any key to exit...
    pause >nul
    exit /b 1
)

:: Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⏳ Installing PyQt6...    ║
    python -m pip install PyQt6 >nul
    if %errorlevel% neq 0 (
        echo    ║  ❌ Failed to install PyQt6 ║
        echo    ╚══════════════════════════════╝
        echo.
        echo    [ERROR] Failed to install PyQt6
        echo    This might be due to:
        echo    1. Permission issues
        echo    2. Corrupted Python installation
        echo    3. Antivirus blocking the installation
        echo.
        echo    Please try:
        echo    1. Running as administrator
        echo    2. Temporarily disabling antivirus
        echo    3. Reinstalling Python
        echo.
        echo    Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo    ║  ✅ PyQt6 installed        ║
) else (
    echo    ║  ✅ PyQt6 installed        ║
)

:: Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⏳ Installing pywin32...  ║
    python -m pip install pywin32 >nul
    if %errorlevel% neq 0 (
        echo    ║  ❌ Failed to install pywin32 ║
        echo    ╚══════════════════════════════╝
        echo.
        echo    [ERROR] Failed to install pywin32
        echo    This might be due to:
        echo    1. Permission issues
        echo    2. Corrupted Python installation
        echo    3. Antivirus blocking the installation
        echo.
        echo    Please try:
        echo    1. Running as administrator
        echo    2. Temporarily disabling antivirus
        echo    3. Reinstalling Python
        echo.
        echo    Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo    ║  ✅ pywin32 installed      ║
) else (
    echo    ║  ✅ pywin32 installed      ║
)

:: Check if the main script exists
if not exist cat_companion.py (
    echo    ║  ❌ Main script missing     ║
    echo    ╚══════════════════════════════╝
    echo.
    echo    [ERROR] cat_companion.py not found
    echo    Please make sure the script is in the same folder
    echo    as this batch file
    echo.
    echo    Press any key to exit...
    pause >nul
    exit /b 1
)

echo    ╚══════════════════════════════╝
echo.

:: Print starting message with animation
echo    Starting Cat Companion...
echo    [░░░░░░░░░░░░░░░░░░░░] 0%%
timeout /t 1 /nobreak >nul
echo    [▓▓░░░░░░░░░░░░░░░░░░] 20%%
timeout /t 1 /nobreak >nul
echo    [▓▓▓▓░░░░░░░░░░░░░░░░] 40%%
timeout /t 1 /nobreak >nul
echo    [▓▓▓▓▓▓░░░░░░░░░░░░░░] 60%%
timeout /t 1 /nobreak >nul
echo    [▓▓▓▓▓▓▓▓░░░░░░░░░░░░] 80%%
timeout /t 1 /nobreak >nul
echo    [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%%
echo.

:: Start the application and minimize the window
start /min python cat_companion.py

:: Wait a moment for the application to start
timeout /t 2 /nobreak >nul

:: Minimize this window
powershell -window minimized -command "& {[System.Windows.Forms.SendKeys]::SendWait('{F11}')}" 
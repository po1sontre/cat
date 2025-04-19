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
    echo    ║  Please install Python     ║
    echo    ╚══════════════════════════════╝
    echo.
    pause
    exit /b 1
) else (
    echo    ║  ✅ Python installed       ║
)

:: Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⏳ Installing PyQt6...    ║
    pip install PyQt6 >nul
    echo    ║  ✅ PyQt6 installed        ║
) else (
    echo    ║  ✅ PyQt6 installed        ║
)

:: Check if pywin32 is installed
python -c "import win32api" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⏳ Installing pywin32...  ║
    pip install pywin32 >nul
    echo    ║  ✅ pywin32 installed      ║
) else (
    echo    ║  ✅ pywin32 installed      ║
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
timeout /t 1 /nobreak >nobreak >nul
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
@echo off
setlocal enabledelayedexpansion
title Cat Companion Setup
color 0D
mode con: cols=60 lines=30

:: Create application directory if it doesn't exist
set "APP_DIR=%USERPROFILE%\CatCompanion"
if not exist "%APP_DIR%" (
    mkdir "%APP_DIR%" 2>nul
    if !errorlevel! neq 0 (
        set "APP_DIR=%CD%"
    )
)

:: Set log file path
set "LOG_FILE=%APP_DIR%\cat_companion_setup.log"

:: Create detailed log file header
echo ======================= CAT COMPANION SETUP LOG ======================= > "%LOG_FILE%"
echo Started: %date% %time% >> "%LOG_FILE%"
echo Working Directory: %CD% >> "%LOG_FILE%"
echo User: %USERNAME% >> "%LOG_FILE%"
echo Computer: %COMPUTERNAME% >> "%LOG_FILE%"
echo Windows Version: >> "%LOG_FILE%"
ver >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo System PATH: >> "%LOG_FILE%"
echo %PATH% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo ================================================================= >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

:: Function to log steps, info and errors 
:log
echo [%date% %time%] %~1 >> "%LOG_FILE%"
exit /b

:: Function to log errors with detailed information
:log_error
echo [%date% %time%] ERROR: %~1 >> "%LOG_FILE%"
echo Error Details: %~2 >> "%LOG_FILE%"
echo Error Code: %errorlevel% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
exit /b

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

:: Print status box header
echo    ╔══════════════════════════════╗
echo    ║        Setup Progress        ║
echo    ╠══════════════════════════════╣

:: Check admin privileges
call :log "Checking admin privileges"
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo    ║  ⚠️ Not running as admin      ║
    call :log "Not running with admin privileges - continuing anyway"
) else (
    echo    ║  ✅ Running as admin         ║
    call :log "Running with admin privileges"
)

:: Check if we can write to the current directory
call :log "Checking write permissions"
echo test > test_write_permission.tmp 2>nul
if %errorlevel% neq 0 (
    echo    ║  ⚠️ Limited write permissions ║
    call :log_error "Limited write permissions" "Failed to write test file"
    set "APP_DIR=%TEMP%\CatCompanion"
    mkdir "%APP_DIR%" 2>nul
    echo    ║  ℹ️ Using temp directory     ║
    call :log "Using temporary directory: %APP_DIR%"
) else (
    del test_write_permission.tmp >nul 2>&1
    echo    ║  ✅ Write permissions OK     ║
    call :log "Write permissions OK"
)

:: Check if Python is installed and in PATH
call :log "Checking for Python"
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ❌ Python not found        ║
    call :log_error "Python not found" "Python command not found in PATH"
    
    :: Try to find Python in common install locations
    call :log "Searching for Python in common locations"
    for %%G in (
        "%ProgramFiles%\Python*\python.exe"
        "%ProgramFiles(x86)%\Python*\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    ) do (
        if exist "%%G" (
            echo    ║  ℹ️ Found Python at:        ║
            echo    ║  %%G                 ║
            call :log "Found Python at: %%G"
            set "PYTHON_PATH=%%G"
            goto :python_found
        )
    )
    
    :: Also try with py launcher
    call :log "Checking for py launcher"
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo    ║  ℹ️ Found Python launcher    ║
        call :log "Found Python launcher"
        set "PYTHON_CMD=py"
        goto :python_launcher_found
    )
    
    :: Python not found anywhere, offer to download
    echo    ║                            ║
    echo    ║  Please install Python 3.8+ ║
    echo    ║  from python.org           ║
    echo    ╚══════════════════════════════╝
    echo.
    echo    Opening Python download page...
    call :log "Opening Python download page"
    start https://www.python.org/downloads/
    echo.
    echo    [ERROR] Python is required to run Cat Companion
    echo    Please install Python 3.8 or higher from python.org
    echo    IMPORTANT: During installation:
    echo    1. Check "Add Python to PATH"
    echo    2. Choose "Install Now" (not "Customize")
    echo    3. After installation, RESTART your computer
    echo.
    echo    Press any key to exit...
    pause >nul
    exit /b 1
) else (
    echo    ║  ✅ Python installed       ║
    call :log "Python found in PATH"
    set "PYTHON_CMD=python"
)

:python_found
if defined PYTHON_PATH (
    set "PYTHON_CMD=%PYTHON_PATH%"
)

:python_launcher_found
:: Check Python version
call :log "Checking Python version"
%PYTHON_CMD% -c "import sys; print('Python version: ' + '.'.join(map(str, sys.version_info[:3])))" >> "%LOG_FILE%" 2>&1
%PYTHON_CMD% -c "import sys; v=sys.version_info; exit(0 if v[0]>=3 and v[1]>=8 else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⚠️ Python version < 3.8    ║
    call :log_error "Python version too old" "Version less than 3.8"
) else (
    echo    ║  ✅ Python 3.8+ verified   ║
    call :log "Python version 3.8+ verified"
)

:: Get detailed Python info
%PYTHON_CMD% -c "import sys, os; print(f'Python executable: {sys.executable}'); print(f'Site packages: {os.path.join(os.path.dirname(os.path.dirname(sys.executable)), \"Lib\", \"site-packages\")}');" >> "%LOG_FILE%" 2>&1

:: Check if pip is installed
call :log "Checking for pip"
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ❌ pip not found          ║
    echo    ║  Installing pip...         ║
    call :log "Pip not found, attempting to install"
    
    :: Try different methods to install pip
    %PYTHON_CMD% -m ensurepip --default-pip >nul 2>&1
    if %errorlevel% neq 0 (
        :: Try downloading get-pip.py
        echo    ║  ⏳ Downloading pip installer ║
        call :log "Downloading get-pip.py"
        powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'" >nul 2>&1
        if %errorlevel% neq 0 (
            echo    ║  ❌ Failed to download pip  ║
            echo    ╚══════════════════════════════╝
            echo.
            echo    [ERROR] Failed to install pip
            echo    This might be due to:
            echo    1. No internet connection
            echo    2. Firewall blocking access
            echo    3. Python installation is corrupted
            echo.
            echo    Press any key to exit...
            pause >nul
            call :log_error "Failed to download get-pip.py" "Download failed"
            exit /b 1
        )
        
        :: Run get-pip.py
        echo    ║  ⏳ Running pip installer    ║
        call :log "Running get-pip.py"
        %PYTHON_CMD% get-pip.py >nul 2>&1
        if %errorlevel% neq 0 (
            echo    ║  ❌ Failed to install pip  ║
            echo    ╚══════════════════════════════╝
            echo.
            echo    [ERROR] Failed to install pip
            echo    This might be due to:
            echo    1. Permission issues
            echo    2. Python installation problems
            echo    3. Antivirus blocking the process
            echo.
            echo    Press any key to exit...
            pause >nul
            call :log_error "Failed to install pip with get-pip.py" "Installation failed"
            exit /b 1
        )
        del get-pip.py >nul 2>&1
    )
    
    :: Verify pip installation
    %PYTHON_CMD% -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo    ║  ❌ Pip install failed     ║
        echo    ╚══════════════════════════════╝
        echo.
        echo    [ERROR] All attempts to install pip failed
        echo    Please try:
        echo    1. RESTART your computer
        echo    2. Reinstall Python (check "Add Python to PATH")
        echo    3. Run this script as administrator
        echo.
        echo    Press any key to exit...
        pause >nul
        call :log_error "All pip installation methods failed" "Pip not available after attempts"
        exit /b 1
    ) else (
        echo    ║  ✅ pip installed          ║
        call :log "Pip successfully installed"
    )
) else (
    echo    ║  ✅ pip installed          ║
    call :log "Pip already installed"
    %PYTHON_CMD% -m pip --version >> "%LOG_FILE%" 2>&1
)

:: Check pip is up to date
call :log "Updating pip"
echo    ║  ⏳ Updating pip...         ║
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
if %errorlevel% equ 0 (
    echo    ║  ✅ pip updated           ║
    call :log "Pip updated successfully"
) else (
    echo    ║  ⚠️ pip update failed      ║
    call :log_error "Pip update failed" "Update command failed"
)

:: Check internet connection
call :log "Checking internet connection"
ping -n 1 -w 1000 8.8.8.8 >nul 2>&1
if %errorlevel% neq 0 (
    ping -n 1 -w 1000 google.com >nul 2>&1
)
if %errorlevel% neq 0 (
    echo    ║  ⚠️ Limited connectivity    ║
    call :log_error "Limited connectivity" "Failed to ping Google DNS"
    
    :: Try to connect to Python package index
    echo    ║  ⏳ Testing PyPI access...   ║
    %PYTHON_CMD% -c "import urllib.request; urllib.request.urlopen('https://pypi.org', timeout=5)" >nul 2>&1
    if %errorlevel% neq 0 (
        echo    ║  ❌ No PyPI access         ║
        echo    ╚══════════════════════════════╝
        echo.
        echo    [ERROR] Cannot connect to Python Package Index
        echo    Cat Companion needs internet to install required packages
        echo    Please check your connection and try again
        echo.
        echo    Press any key to exit...
        pause >nul
        call :log_error "No PyPI access" "Cannot connect to Python Package Index"
        exit /b 1
    ) else (
        echo    ║  ✅ PyPI access OK         ║
        call :log "PyPI access verified despite network test failure"
    )
) else (
    echo    ║  ✅ Internet connected      ║
    call :log "Internet connection verified"
)

:: Check if required packages can be installed
call :log "Checking/installing required packages"

:: Function to install Python package
:install_package
set "package_name=%~1"
set "import_name=%~2"
if "%import_name%"=="" set "import_name=%package_name%"

call :log "Checking for %package_name%"
%PYTHON_CMD% -c "import %import_name%" >nul 2>&1
if %errorlevel% neq 0 (
    echo    ║  ⏳ Installing %package_name%...    ║
    call :log "Installing %package_name%"
    %PYTHON_CMD% -m pip install %package_name% >> "%LOG_FILE%" 2>&1
    if %errorlevel% neq 0 (
        echo    ║  ❌ Failed to install %package_name% ║
        call :log_error "Failed to install %package_name%" "pip install failed"
        
        :: Try alternative installation method with --user flag
        echo    ║  ⏳ Trying alternative install.. ║
        call :log "Trying alternative install method for %package_name%"
        %PYTHON_CMD% -m pip install --user %package_name% >> "%LOG_FILE%" 2>&1
        if %errorlevel% neq 0 (
            echo    ║  ❌ All install methods failed ║
            call :log_error "All install methods failed for %package_name%" "Both standard and --user installs failed"
            set "INSTALL_FAILED=1"
            exit /b 1
        ) else (
            echo    ║  ✅ %package_name% installed (alt)   ║
            call :log "%package_name% installed with alternative method"
        )
    ) else (
        echo    ║  ✅ %package_name% installed        ║
        call :log "%package_name% installed successfully"
    )
) else (
    echo    ║  ✅ %package_name% already installed ║
    call :log "%package_name% already installed"
)
exit /b 0

:: Install required packages
set "INSTALL_FAILED=0"
call :install_package PyQt6
if "%INSTALL_FAILED%"=="1" goto :package_install_failed

call :install_package pywin32 win32api
if "%INSTALL_FAILED%"=="1" goto :package_install_failed

:: Check if the main script exists or needs to be created
if not exist cat_companion.py (
    echo    ║  ⚠️ Main script missing     ║
    call :log_error "Main script missing" "cat_companion.py not found"
    
    :: Try to download or create a basic script
    echo    ║  ⏳ Creating basic script...  ║
    call :log "Creating basic cat_companion.py script"
    
    echo import sys > cat_companion.py
    echo from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget >> cat_companion.py
    echo from PyQt6.QtCore import Qt >> cat_companion.py
    echo. >> cat_companion.py
    echo class CatCompanion(QMainWindow): >> cat_companion.py
    echo     def __init__(self): >> cat_companion.py
    echo         super().__init__() >> cat_companion.py
    echo         self.setWindowTitle("Cat Companion") >> cat_companion.py
    echo         self.setGeometry(100, 100, 400, 300) >> cat_companion.py
    echo. >> cat_companion.py
    echo         # Create central widget and layout >> cat_companion.py
    echo         central_widget = QWidget() >> cat_companion.py
    echo         layout = QVBoxLayout(central_widget) >> cat_companion.py
    echo. >> cat_companion.py
    echo         # Add welcome label >> cat_companion.py
    echo         welcome_label = QLabel("Welcome to Cat Companion!") >> cat_companion.py
    echo         welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter) >> cat_companion.py
    echo         layout.addWidget(welcome_label) >> cat_companion.py
    echo. >> cat_companion.py
    echo         # Add cat emoji >> cat_companion.py
    echo         cat_label = QLabel("🐱") >> cat_companion.py
    echo         cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter) >> cat_companion.py
    echo         cat_label.setStyleSheet("font-size: 72px;") >> cat_companion.py
    echo         layout.addWidget(cat_label) >> cat_companion.py
    echo. >> cat_companion.py
    echo         # Set central widget >> cat_companion.py
    echo         self.setCentralWidget(central_widget) >> cat_companion.py
    echo. >> cat_companion.py
    echo if __name__ == "__main__": >> cat_companion.py
    echo     app = QApplication(sys.argv) >> cat_companion.py
    echo     window = CatCompanion() >> cat_companion.py
    echo     window.show() >> cat_companion.py
    echo     sys.exit(app.exec()) >> cat_companion.py
    
    if exist cat_companion.py (
        echo    ║  ✅ Basic script created    ║
        call :log "Basic cat_companion.py script created successfully"
    ) else (
        echo    ║  ⚠️ Could not create script ║
        call :log_error "Could not create script" "Failed to create cat_companion.py"
    )
) else (
    echo    ║  ✅ Main script exists      ║
    call :log "Main script cat_companion.py found"
)

echo    ╚══════════════════════════════╝
echo.
goto :start_application

:package_install_failed
echo    ╚══════════════════════════════╝
echo.
echo    [ERROR] Failed to install required packages
echo    Please check %LOG_FILE% for details
echo    Common issues:
echo    1. Internet connection problems
echo    2. Firewall blocking access to PyPI
echo    3. Permission issues (try running as administrator)
echo    4. Antivirus blocking installation
echo.
echo    Press any key to exit...
pause >nul
exit /b 1

:start_application
call :log "Starting application"

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

:: Create a wrapper script to handle potential exceptions
echo import sys, traceback > run_cat_companion.py
echo try: >> run_cat_companion.py
echo     import cat_companion >> run_cat_companion.py
echo except Exception as e: >> run_cat_companion.py
echo     with open('%APP_DIR:\=\\%\\cat_companion_error.log', 'w') as f: >> run_cat_companion.py
echo         f.write(f"Error: {e}\n\n") >> run_cat_companion.py
echo         f.write(traceback.format_exc()) >> run_cat_companion.py
echo     print(f"Error: {e}") >> run_cat_companion.py
echo     input("Press Enter to exit...") >> run_cat_companion.py
echo     sys.exit(1) >> run_cat_companion.py

:: Try to start the application with error handling
echo    Starting application...
call :log "Executing Python script"
%PYTHON_CMD% run_cat_companion.py 2>> "%LOG_FILE%"
if %errorlevel% neq 0 (
    echo    [ERROR] Application crashed
    echo    Please check %LOG_FILE% and %APP_DIR%\cat_companion_error.log for details
    echo    Common issues:
    echo    1. Python installation issues
    echo    2. Missing dependencies
    echo    3. Permission problems
    echo    4. Graphics driver issues
    echo.
    echo    Press any key to exit...
    pause >nul
    call :log_error "Application crashed" "Python script execution failed with error code %errorlevel%"
    exit /b 1
)

:: Remove temporary script
del run_cat_companion.py >nul 2>&1

:: Wait a moment for the application to start
timeout /t 2 /nobreak >nul

:: Minimize this window
call :log "Minimizing console window"
powershell -window minimized -command "& {[System.Windows.Forms.SendKeys]::SendWait('{F11}')}"

endlocal
exit /b 0
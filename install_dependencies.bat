@echo off
echo Checking for Python 3 and pip/pip3 installation...

REM Check if Python 3 is installed
where python >nul 2>&1
if %errorlevel% equ 0 (
    python --version | find "Python 3" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Python 3 is installed.
    ) else (
        echo Python 3 is not installed.
        echo Please install Python 3 from https://www.python.org/downloads/
        pause
        exit /b 1
    )
) else (
    echo Python is not installed.
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is installed
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo pip is installed.
    set PIP_COMMAND=pip
) else (
    where pip3 >nul 2>&1
    if %errorlevel% equ 0 (
        echo pip3 is installed.
        set PIP_COMMAND=pip3
    ) else (
        echo Neither pip nor pip3 is installed.
        echo Please ensure pip is installed with Python 3.
        echo You can install it by running: python -m ensurepip --upgrade
        pause
        exit /b 1
    )
)

echo Python 3 and pip/pip3 are installed and ready to use.

REM Install ChromeDriver
echo Installing ChromeDriver...

REM Get the latest ChromeDriver version
for /f "delims=" %%i in ('powershell -command "(Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE').Content"') do set LATEST_CHROMEDRIVER=%%i

REM Download the latest ChromeDriver
echo Downloading ChromeDriver version %LATEST_CHROMEDRIVER%...
powershell -command "Invoke-WebRequest -Uri 'https://chromedriver.storage.googleapis.com/%LATEST_CHROMEDRIVER%/chromedriver_win32.zip' -OutFile 'chromedriver_win32.zip'"

REM Unzip the downloaded file
echo Extracting ChromeDriver...
powershell -command "Expand-Archive -Path 'chromedriver_win32.zip' -DestinationPath '.' -Force"

REM Move ChromeDriver to a directory in the PATH (e.g., C:\Windows\System32)
echo Moving ChromeDriver to C:\Windows\System32...
move /Y chromedriver.exe C:\Windows\System32\chromedriver.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to move ChromeDriver to C:\Windows\System32. Ensure you have administrator privileges.
    pause
    exit /b 1
)

REM Clean up
echo Cleaning up...
del chromedriver_win32.zip >nul 2>&1

echo ChromeDriver installation complete.

REM Install Python dependencies
echo Installing Python dependencies...
%PIP_COMMAND% install requests beautifulsoup4 selenium webdriver-manager flask Flask-HTTPAuth
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies. Check your internet connection or pip configuration.
    pause
    exit /b 1
)

echo All dependencies installed successfully!
pause
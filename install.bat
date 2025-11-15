@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_INSTALLER_PATH=%SCRIPT_DIR%data\\packages\\python-3.11.0-amd64.exe"

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found, installing...
    if not exist "%PYTHON_INSTALLER_PATH%" (
        echo ERROR: Python installer not found at %PYTHON_INSTALLER_PATH%
        echo Please place the Python installer in the specified directory.
        exit /b 1
    )
    "%PYTHON_INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo Python installed successfully.
) else (
    echo Python is already installed.
)

echo Running Python installer script...
python "%SCRIPT_DIR%scripts\\installer.py"
pause

endlocal

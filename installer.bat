@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_INSTALLER_PATH=%SCRIPT_DIR%data\\packages\\python-3.11.0-amd64.exe"
set "GTK_INSTALLER_PATH=%SCRIPT_DIR%data\\packages\\gtk-runtime-3.8.1-i686.exe"
set "GTK_VENDOR_PATH=%SCRIPT_DIR%vendor\\gtk-windows"

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

if exist "%GTK_VENDOR_PATH%" (
    echo GTK runtime already installed.
    goto :eof
)

if not exist "%GTK_INSTALLER_PATH%" (
    echo ERROR: GTK installer not found at %GTK_INSTALLER_PATH%
    echo Please place the GTK installer in the specified directory.
    exit /b 1
)

echo Installing GTK runtime...
"%GTK_INSTALLER_PATH%" /S /D=%GTK_VENDOR_PATH%

echo GTK runtime installed successfully.

set "JSON_FILE=%SCRIPT_DIR%data\\tree.json"

echo Creating/Replacing default tree.json...
(
    echo [
    echo     {
    echo         "text": "Root",
    echo         "children": [
    echo             {
    echo                 "text": "Child 1",
    echo                 "children": [
    echo                     {
    echo                         "text": "Grandchild 1",
    echo                         "children": []
    echo                     }
    echo                 ]
    echo             },
    echo             {
    echo                 "text": "Child 2",
    echo                 "children": []
    echo             }
    echo         ]
    echo     }
    echo ]
) > "%JSON_FILE%"
echo tree.json created successfully.

endlocal

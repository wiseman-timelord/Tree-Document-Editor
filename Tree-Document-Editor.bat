@echo off
setlocal enabledelayedexpansion

:: Change to the script's directory to ensure proper path resolution
cd /d "%~dp0"

set "SCRIPT_DIR=%~dp0"
set "GTK_PATH=%SCRIPT_DIR%vendor\\gtk-windows\\bin"
set "PYTHONPATH=%SCRIPT_DIR%vendor\\gtk-windows\\lib\\site-packages"
set "GI_TYPELIB_PATH=%SCRIPT_DIR%vendor\\gtk-windows\\lib\\girepository-1.0"
set "PATH=%GTK_PATH%;%PATH%"

:MAIN_MENU
cls
echo ===============================================================================
echo    Tree-Document-Editor: Batch Menu
echo ===============================================================================
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo    1) Launch Tree-Document-Editor
echo.
echo    2) Install Requirements
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo -------------------------------------------------------------------------------
set /p choice="Selection; Menu Options = 1-2, Quit Program = Q: "

if /i "%choice%"=="1" call :LAUNCH
if /i "%choice%"=="2" call :INSTALL
if /i "%choice%"=="Q" call :QUIT
if /i "%choice%"=="1" goto MAIN_MENU
if /i "%choice%"=="2" goto MAIN_MENU
if /i "%choice%"=="Q" exit /b 0
echo Invalid selection. Please try again.
pause
goto MAIN_MENU

:LAUNCH
cls
echo ===============================================================================
echo    Launching Tree-Document-Editor
echo ===============================================================================
echo.
echo Starting application...
python "%SCRIPT_DIR%scripts\\editor.py"
echo.
pause
goto :eof

:INSTALL
cls
echo ===============================================================================
echo    Installing Requirements
echo ===============================================================================
echo.
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
echo.
echo Running Python installer script...
python "%SCRIPT_DIR%scripts\\installer.py" windows
echo.
echo Installation complete.
pause
goto :eof

:QUIT
cls
echo ===============================================================================
echo    Exiting Program
echo ===============================================================================
echo.
echo Exiting program...
echo Thank you for using Tree-Document-Editor.
echo.
timeout /t 2 /nobreak >nul
goto :eof

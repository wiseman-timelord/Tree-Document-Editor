@echo off
set "SCRIPT_DIR=%~dp0"
set "GTK_PATH=%SCRIPT_DIR%vendor\\gtk-windows"
set "PATH=%GTK_PATH%\\bin;%PATH%"
set "PYTHONPATH=%GTK_PATH%\\lib\\site-packages"
set "GI_TYPELIB_PATH=%GTK_PATH%\\lib\\girepository-1.0"
python "%SCRIPT_DIR%scripts\\editor.py"

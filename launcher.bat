@echo off
set "GTK_PATH=%~dp0vendor\\gtk-windows\\bin"
set "PATH=%GTK_PATH%;%PATH%"
python scripts/editor.py

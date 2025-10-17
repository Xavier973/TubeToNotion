@echo off

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

rem Utiliser directement le python du venv pour être sûr du bon interpréteur
call "%SCRIPT_DIR%venv\Scripts\python.exe" "%SCRIPT_DIR%main.py"

pause
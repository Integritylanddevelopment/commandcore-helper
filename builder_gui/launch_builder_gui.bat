@echo off
REM Launch the builder GUI
cd /d "%~dp0"
python builder_gui.py
pause
REM This script is used to launch the Builder GUI.
REM Make sure to run this script from the CommandCore root directory.
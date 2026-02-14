@echo off
title Luotianyi Desktop Pet

echo ========================================
echo       Luotianyi Desktop Pet v1.0
echo ========================================
echo.

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.7+
    echo Download: www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Starting Luotianyi Desktop Pet...
echo Press ESC to exit
echo.

python main.py

if errorlevel 1 (
    echo.
    echo Failed to start, please check:
    echo 1. All dependencies installed
    echo 2. Run as administrator
    echo 3. System supports transparent windows
    echo.
    pause
)

exit /b 0
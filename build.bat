@echo off
title Build Luotianyi Desktop Pet

echo ========================================
echo   Building Luotianyi Desktop Pet
echo ========================================
echo.

echo Step 1: Installing PyInstaller...
pip install pyinstaller
echo.

echo Step 2: Packaging...
pyinstaller --noconfirm --clean luotianyi.spec
echo.

if errorlevel 1 (
    echo Build FAILED!
    pause
    exit /b 1
)

echo Step 3: Done!
echo.
echo Output: dist\LuotianyiPet\
echo EXE:    dist\LuotianyiPet\LuotianyiPet.exe
echo.
echo Send the entire "dist\LuotianyiPet" folder to your friend.
echo Or compress it to a zip file first.
echo.
pause

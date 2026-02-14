@echo off
REM Universal Setup Script for Human Detection Camera - Windows
REM Automatically installs all required Python packages

echo ==========================================
echo Human Detection Camera - Windows Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python is installed:
python --version
echo.

echo Installing required packages...
echo.

REM Install packages using pip
echo Installing opencv-python...
python -m pip install opencv-python
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install opencv-python
)

echo Installing numpy...
python -m pip install numpy
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install numpy
)

echo Installing PyQt5...
python -m pip install PyQt5
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install PyQt5
)

echo Installing pynput...
python -m pip install pynput
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install pynput
)

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo You can now run the application:
echo   python human_detection_app.py
echo.
echo Or double-click on: run_app.bat
echo.
pause
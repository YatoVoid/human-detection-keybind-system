@echo off
REM Quick launcher for Human Detection Camera on Windows

echo Starting Human Detection Camera...
python human_detection_app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed or failed to start
    echo.
    pause
)
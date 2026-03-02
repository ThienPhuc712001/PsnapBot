@echo off
echo Installing PSnapBOT - Local Persistent Development Agent...
echo.

REM Set Python path
set PYTHON_PATH="C:\Users\cntt.tts13\AppData\Local\Microsoft\WindowsApps\python3.exe"

echo Using Python at: %PYTHON_PATH%
echo.

REM Check if Python exists
if not exist %PYTHON_PATH% (
    echo Error: Python not found at expected location
    echo Please check Python installation
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

REM Install dependencies
%PYTHON_PATH% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

echo Testing PSnapBOT...
echo.

%PYTHON_PATH% test_agent.py

echo.
echo Installation complete!
echo.
echo To run PSnapBOT:
echo   %PYTHON_PATH% main.py
echo.
pause
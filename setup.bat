@echo off
echo Setting up PSnapBOT - Local Persistent Development Agent...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

echo Python found, installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Testing the agent...
python test_agent.py

echo.
echo Setup complete! You can now run the agent with:
echo   python main.py
echo.
pause
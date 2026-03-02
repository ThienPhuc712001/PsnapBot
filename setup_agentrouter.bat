@echo off
setlocal enabledelayedexpansion
echo Setting up PSnapBOT with AgentRouter...
echo.

REM Try different Python paths
for %%P in (
    "python3"
    "python"
    "py"
    "C:\Python314\python.exe"
    "C:\Python314\Scripts\python.exe"
    "C:\Users\cntt.tts13\AppData\Local\Microsoft\WindowsApps\python3.exe"
) do (
    echo Trying Python: %%P
    %%P --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo Found Python: %%P
        echo.
        echo Installing dependencies...
        %%P -m pip install -r requirements.txt
        if !errorlevel! equ 0 (
            echo.
            echo Dependencies installed successfully!
            echo.
            echo PSnapBOT with AgentRouter is ready to use!
            echo.
            echo To run PSnapBOT:
            echo   py main.py
            echo.
            echo Or use: run_psnappbot.bat
            echo.
            echo Your API key is already configured in config_agentrouter.py
        ) else (
            echo Error: Failed to install dependencies
        )
        goto :end
    )
)

echo Python not found! Please install Python 3.10+ and add to PATH.
echo Visit: https://www.python.org/downloads/

:end
pause
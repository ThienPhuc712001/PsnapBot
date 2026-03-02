@echo off
echo Starting PSnapBOT - Local Persistent Development Agent...
echo.

REM Set Python path
set PYTHON_PATH="C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe"

echo Using Python at: %PYTHON_PATH%
echo.

REM Change to dev_agent directory
cd /d "d:\PsnapBot\dev_agent"

REM Run PSnapBOT
%PYTHON_PATH% main.py %*

echo.
echo PSnapBOT stopped.
pause
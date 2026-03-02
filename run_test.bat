@echo off
setlocal enabledelayedexpansion
echo Testing PSnapBOT Connection...
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
        %%P test_connection.py
        goto :end
    )
)

echo Python not found! Please install Python 3.10+ and add to PATH.
echo.

:end
pause
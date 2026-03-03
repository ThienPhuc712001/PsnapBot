@echo off
title PSnapBOT - GO!

:: The simplest way to run PSnapBOT
echo ============================================================
echo                    PSnapBOT - GO!
echo ============================================================
echo.
echo [1] Quick Test (Hello World + Demo)
echo [2] Full Test Suite
echo [3] PSnapBOT Interactive Mode
echo [4] Exit
echo.
set /p choice="Choose (1-4): "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto interactive
if "%choice%"=="4" goto exit

:quick
echo.
echo [QUICK TEST] Running essential tests...
echo.
echo [1/2] Hello World:
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py
echo.
echo [2/2] PSnapBOT Demo:
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" demo_final.py"
echo.
echo [DONE] Quick test completed!
pause
exit

:full
echo.
echo [FULL TEST] Running complete test suite...
call ALL_IN_ONE.bat
exit

:interactive
echo.
echo [INTERACTIVE] Starting PSnapBOT...
call run_psnappbot.bat --project .
exit

:exit
echo.
echo [BYE] See you next time!
exit
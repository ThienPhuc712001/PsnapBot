@echo off
title PSnapBOT - Quick Runner

:: Quick menu for PSnapBOT commands
:menu
cls
echo ============================================================
echo                PSnapBOT - Quick Runner
echo ============================================================
echo.
echo 1. Run Hello World Test
echo 2. Run Offline Demo
echo 3. Test API Connection
echo 4. Show PSnapBOT Info
echo 5. Show PSnapBOT Status
echo 6. Run Final Demo
echo 7. Run All Tests
echo 8. Exit
echo.
set /p choice="Choose option (1-8): "

if "%choice%"=="1" goto test1
if "%choice%"=="2" goto test2
if "%choice%"=="3" goto test3
if "%choice%"=="4" goto test4
if "%choice%"=="5" goto test5
if "%choice%"=="6" goto test6
if "%choice%"=="7" goto test7
if "%choice%"=="8" goto exit
goto menu

:test1
echo.
echo [RUNNING] Hello World Test...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py
pause
goto menu

:test2
echo.
echo [RUNNING] Offline Demo...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_offline_demo.py"
pause
goto menu

:test3
echo.
echo [RUNNING] API Connection Test...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py"
pause
goto menu

:test4
echo.
echo [RUNNING] PSnapBOT Info...
call run_psnappbot.bat --project . --info
pause
goto menu

:test5
echo.
echo [RUNNING] PSnapBOT Status...
call run_psnappbot.bat --project . --status
pause
goto menu

:test6
echo.
echo [RUNNING] Final Demo...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" demo_final.py"
pause
goto menu

:test7
echo.
echo [RUNNING] All Tests...
call ALL_IN_ONE.bat
pause
goto menu

:exit
echo.
echo [EXIT] Goodbye!
exit
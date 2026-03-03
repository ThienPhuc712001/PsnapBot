@echo off
title PSnapBOT - Work Mode
echo [WORK] PSnapBOT Development Assistant
echo.

:work_menu
cls
echo ============================================================
echo                PSnapBOT - Work Mode
echo ============================================================
echo.
echo [QUICK ACTIONS]
echo   1. Chat with PSnapBOT
echo   2. Fix current issue
echo   3. Add new feature
echo   4. Analyze code
echo   5. Run tests
echo   6. Generate docs
echo   7. Custom command
echo   8. Exit
echo.
set /p work_choice="Choose action (1-8): "

if "%work_choice%"=="1" goto chat
if "%work_choice%"=="2" goto fix
if "%work_choice%"=="3" goto add
if "%work_choice%"=="4" goto analyze
if "%work_choice%"=="5" goto test
if "%work_choice%"=="6" goto docs
if "%work_choice%"=="7" goto custom
if "%work_choice%"=="8" goto exit
goto work_menu

:chat
echo.
call CHAT.bat
goto work_menu

:fix
echo.
call FIX.bat
goto work_menu

:add
echo.
call ADD.bat
goto work_menu

:analyze
echo.
echo [ANALYZE] What would you like to analyze?
echo   1. Current project
echo   2. Specific file
echo   3. Recent changes
echo.
set /p analyze_choice="Choose (1-3): "
if "%analyze_choice%"=="1" call run_psnappbot.bat --project . "Analyze the current project structure and code quality"
if "%analyze_choice%"=="2" (
    set /p file_to_analyze="Enter file path: "
    call run_psnappbot.bat --project . "Analyze file: %file_to_analyze%"
)
if "%analyze_choice%"=="3" call run_psnappbot.bat --project . "Analyze recent changes and their impact"
goto work_menu

:test
echo.
echo [TEST] Running comprehensive test suite...
call run_psnappbot.bat --project . "Run all tests and fix any failures"
goto work_menu

:docs
echo.
echo [DOCS] Generating documentation...
call run_psnappbot.bat --project . "Generate comprehensive documentation for this project"
goto work_menu

:custom
echo.
set /p custom_command="Enter your command: "
if "%custom_command%"=="" goto work_menu
echo.
call run_psnappbot.bat --project . "%custom_command%"
goto work_menu

:exit
echo.
echo [DONE] Work session completed. Your progress has been saved.
timeout /t 2 >nul
exit
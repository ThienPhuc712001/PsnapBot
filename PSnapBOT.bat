@echo off
title PSnapBOT - AI Development Assistant
color 0B

:main_menu
cls
echo ============================================================
echo              PSnapBOT - AI Development Assistant
echo ============================================================
echo.
echo [PROJECT] Current: %CD%
echo.
echo [MODES]
echo   1. Interactive Mode    - Chat with PSnapBOT
echo   2. Quick Command     - Single task execution  
echo   3. Project Setup     - Configure new project
echo   4. Code Analysis     - Analyze current code
echo   5. Build & Fix      - Auto-fix build errors
echo   6. Documentation    - Generate docs
echo   7. System Status    - Check PSnapBOT health
echo   8. Settings         - Configuration
echo   9. Exit
echo.
set /p choice="Choose mode (1-9): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto quick_command
if "%choice%"=="3" goto project_setup
if "%choice%"=="4" goto code_analysis
if "%choice%"=="5" goto build_fix
if "%choice%"=="6" goto documentation
if "%choice%"=="7" goto system_status
if "%choice%"=="8" goto settings
if "%choice%"=="9" goto exit
goto main_menu

:interactive
echo.
echo [INTERACTIVE] Starting PSnapBOT in interactive mode...
echo [TIP] Type 'help' for commands, 'exit' to quit
echo.
call run_psnappbot.bat --project .
pause
goto main_menu

:quick_command
echo.
echo [QUICK COMMAND] Enter your task:
echo [Examples] 
echo   - "Fix the build error in main.py"
echo   - "Add user authentication feature"
echo   - "Refactor the database module"
echo   - "Write unit tests for utils.py"
echo.
set /p command="Task: "
if "%command%"=="" goto main_menu
echo.
echo [EXECUTING] Processing: %command%
call run_psnappbot.bat --project . "%command%"
pause
goto main_menu

:project_setup
echo.
echo [PROJECT SETUP] Configuring PSnapBOT for this project...
echo.
call run_psnappbot.bat --project . "Analyze this project structure and set up development environment"
pause
goto main_menu

:code_analysis
echo.
echo [CODE ANALYSIS] Choose analysis type:
echo   1. Full project analysis
echo   2. Specific file analysis
echo   3. Code quality check
echo   4. Security scan
echo.
set /p analysis_type="Choose (1-4): "

if "%analysis_type%"=="1" (
    call run_psnappbot.bat --project . "Perform comprehensive code analysis of this project"
)
if "%analysis_type%"=="2" (
    set /p file_path="Enter file path: "
    call run_psnappbot.bat --project . "Analyze file: %file_path%"
)
if "%analysis_type%"=="3" (
    call run_psnappbot.bat --project . "Check code quality and suggest improvements"
)
if "%analysis_type%"=="4" (
    call run_psnappbot.bat --project . "Perform security analysis and identify vulnerabilities"
)

pause
goto main_menu

:build_fix
echo.
echo [BUILD & FIX] Auto-fix mode
echo.
echo [OPTIONS]
echo   1. Fix current build errors
echo   2. Run tests and fix failures
echo   3. Optimize build performance
echo.
set /p build_option="Choose (1-3): "

if "%build_option%"=="1" (
    call run_psnappbot.bat --project . "Fix all build errors automatically"
)
if "%build_option%"=="2" (
    call run_psnappbot.bat --project . "Run tests and fix any failures"
)
if "%build_option%"=="3" (
    call run_psnappbot.bat --project . "Optimize build performance and dependencies"
)

pause
goto main_menu

:documentation
echo.
echo [DOCUMENTATION] Generate project documentation
echo.
echo [OPTIONS]
echo   1. Generate README
echo   2. Generate API docs
echo   3. Generate code comments
echo   4. Create technical documentation
echo.
set /p doc_option="Choose (1-4): "

if "%doc_option%"=="1" (
    call run_psnappbot.bat --project . "Generate comprehensive README.md for this project"
)
if "%doc_option%"=="2" (
    call run_psnappbot.bat --project . "Generate API documentation from code"
)
if "%doc_option%"=="3" (
    call run_psnappbot.bat --project . "Add detailed comments to all code files"
)
if "%doc_option%"=="4" (
    call run_psnappbot.bat --project . "Create complete technical documentation"
)

pause
goto main_menu

:system_status
echo.
echo [SYSTEM STATUS] Checking PSnapBOT health...
echo.
call run_psnappbot.bat --project . --status
echo.
echo [MEMORY] Checking database status...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_offline_demo.py"
echo.
echo [API] Testing connection...
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py"
pause
goto main_menu

:settings
echo.
echo [SETTINGS] Configuration options
echo.
echo [OPTIONS]
echo   1. View current configuration
echo   2. Test API connection
echo   3. Reset memory database
echo   4. Update API key
echo.
set /p setting_option="Choose (1-4): "

if "%setting_option%"=="1" (
    echo.
    echo [CURRENT CONFIGURATION]
    type config_user.py
    echo.
)
if "%setting_option%"=="2" (
    echo.
    echo [API TEST]
    "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py"
    echo.
)
if "%setting_option%"=="3" (
    echo.
    echo [RESET MEMORY] This will clear all stored data. Continue? (Y/N)
    set /p confirm=
    if /i "%confirm%"=="Y" (
        del data\memory.db 2>nul
        echo Memory database reset successfully.
    )
)
if "%setting_option%"=="4" (
    echo.
    echo [UPDATE API KEY] Edit config_user.py to update your API key
    notepad config_user.py
)

pause
goto main_menu

:exit
echo.
echo [GOODBYE] PSnapBOT session ended. Your work has been saved.
echo.
timeout /t 3 >nul
exit
@echo off
title PSnapBOT - Quick Fix
echo [FIX] PSnapBOT Auto-Fix Mode
echo.
if "%1"=="" (
    echo [USAGE] FIX.bat [issue_description]
    echo.
    echo [EXAMPLES]
    echo   FIX.bat "build error"
    echo   FIX.bat "test failure"
    echo   FIX.bat "import error"
    echo   FIX.bat "syntax error"
    echo.
    set /p issue="Describe the issue: "
) else (
    set issue=%1
)

echo [FIXING] Issue: %issue%
echo.
call run_psnappbot.bat --project . "Fix %issue% automatically"
echo.
echo [DONE] Fix attempt completed.
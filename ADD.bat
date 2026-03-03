@echo off
title PSnapBOT - Add Feature
echo [ADD] PSnapBOT Feature Development
echo.
if "%1"=="" (
    echo [USAGE] ADD.bat [feature_description]
    echo.
    echo [EXAMPLES]
    echo   ADD.bat "user login system"
    echo   ADD.bat "database connection"
    echo   ADD.bat "API endpoint"
    echo   ADD.bat "file upload feature"
    echo.
    set /p feature="Describe the feature to add: "
) else (
    set feature=%1
)

echo [DEVELOPING] Feature: %feature%
echo.
call run_psnappbot.bat --project . "Implement %feature% with best practices"
echo.
echo [DONE] Feature development completed.
# PSnapBOT Work Mode - PowerShell Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                PSnapBOT - Work Mode" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "[QUICK ACTIONS]" -ForegroundColor Yellow
    Write-Host "  1. Chat with PSnapBOT" -ForegroundColor White
    Write-Host "  2. Fix current issue" -ForegroundColor White
    Write-Host "  3. Add new feature" -ForegroundColor White
    Write-Host "  4. Analyze code" -ForegroundColor White
    Write-Host "  5. Run tests" -ForegroundColor White
    Write-Host "  6. Generate docs" -ForegroundColor White
    Write-Host "  7. Custom command" -ForegroundColor White
    Write-Host "  8. Exit" -ForegroundColor White
    Write-Host ""
}

function Start-Chat {
    Write-Host "[CHAT] Starting PSnapBOT Interactive Mode..." -ForegroundColor Green
    Write-Host "[TIP] You can now chat with PSnapBOT about your project" -ForegroundColor Gray
    Write-Host "[TIP] Type 'help' for available commands" -ForegroundColor Gray
    Write-Host "[TIP] Type 'exit' to quit" -ForegroundColor Gray
    Write-Host ""
    & .\run_psnappbot.bat --project .
}

function Fix-Issue {
    Write-Host "[FIX] PSnapBOT Auto-Fix Mode" -ForegroundColor Green
    $issue = Read-Host "Describe the issue (or press Enter for examples)"
    
    if ([string]::IsNullOrEmpty($issue)) {
        Write-Host "[EXAMPLES]" -ForegroundColor Yellow
        Write-Host "  - build error" -ForegroundColor Gray
        Write-Host "  - test failure" -ForegroundColor Gray
        Write-Host "  - import error" -ForegroundColor Gray
        Write-Host "  - syntax error" -ForegroundColor Gray
        $issue = Read-Host "Describe the issue"
    }
    
    if (-not [string]::IsNullOrEmpty($issue)) {
        Write-Host "[FIXING] Issue: $issue" -ForegroundColor Green
        Write-Host ""
        & .\run_psnappbot.bat --project . "Fix $issue automatically"
        Write-Host ""
        Write-Host "[DONE] Fix attempt completed." -ForegroundColor Green
    }
}

function Add-Feature {
    Write-Host "[ADD] PSnapBOT Feature Development" -ForegroundColor Green
    $feature = Read-Host "Describe the feature to add (or press Enter for examples)"
    
    if ([string]::IsNullOrEmpty($feature)) {
        Write-Host "[EXAMPLES]" -ForegroundColor Yellow
        Write-Host "  - user login system" -ForegroundColor Gray
        Write-Host "  - database connection" -ForegroundColor Gray
        Write-Host "  - API endpoint" -ForegroundColor Gray
        Write-Host "  - file upload feature" -ForegroundColor Gray
        $feature = Read-Host "Describe the feature to add"
    }
    
    if (-not [string]::IsNullOrEmpty($feature)) {
        Write-Host "[DEVELOPING] Feature: $feature" -ForegroundColor Green
        Write-Host ""
        & .\run_psnappbot.bat --project . "Implement $feature with best practices"
        Write-Host ""
        Write-Host "[DONE] Feature development completed." -ForegroundColor Green
    }
}

function Analyze-Code {
    Write-Host "[ANALYZE] Choose analysis type:" -ForegroundColor Green
    Write-Host "  1. Full project analysis" -ForegroundColor White
    Write-Host "  2. Specific file analysis" -ForegroundColor White
    Write-Host "  3. Recent changes" -ForegroundColor White
    $choice = Read-Host "Choose (1-3)"
    
    switch ($choice) {
        "1" { & .\run_psnappbot.bat --project . "Analyze the current project structure and code quality" }
        "2" { 
            $file = Read-Host "Enter file path"
            & .\run_psnappbot.bat --project . "Analyze file: $file"
        }
        "3" { & .\run_psnappbot.bat --project . "Analyze recent changes and their impact" }
        default { Write-Host "[ERROR] Invalid choice" -ForegroundColor Red }
    }
}

function Run-Tests {
    Write-Host "[TEST] Running comprehensive test suite..." -ForegroundColor Green
    & .\run_psnappbot.bat --project . "Run all tests and fix any failures"
}

function Generate-Docs {
    Write-Host "[DOCS] Generating documentation..." -ForegroundColor Green
    & .\run_psnappbot.bat --project . "Generate comprehensive documentation for this project"
}

function Custom-Command {
    $command = Read-Host "Enter your command"
    if (-not [string]::IsNullOrEmpty($command)) {
        Write-Host ""
        & .\run_psnappbot.bat --project . "$command"
    }
}

# Main loop
do {
    Clear-Host
    Show-Menu
    $choice = Read-Host "Choose action (1-8)"
    
    switch ($choice) {
        "1" { Start-Chat }
        "2" { Fix-Issue }
        "3" { Add-Feature }
        "4" { Analyze-Code }
        "5" { Run-Tests }
        "6" { Generate-Docs }
        "7" { Custom-Command }
        "8" { 
            Write-Host ""
            Write-Host "[DONE] Work session completed. Your progress has been saved." -ForegroundColor Green
            break
        }
        default { 
            Write-Host "[ERROR] Invalid choice. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
    
    if ($choice -ne "8") {
        Write-Host ""
        Write-Host "Press any key to continue..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
} while ($choice -ne "8")
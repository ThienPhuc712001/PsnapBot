# PSnapBOT Fix Mode - PowerShell Script
param(
    [string]$Issue = ""
)

Write-Host "[FIX] PSnapBOT Auto-Fix Mode" -ForegroundColor Green

if ([string]::IsNullOrEmpty($Issue)) {
    Write-Host "[USAGE] FIX.ps1 [issue_description]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[EXAMPLES]" -ForegroundColor Yellow
    Write-Host "  .\FIX.ps1 'build error'" -ForegroundColor Gray
    Write-Host "  .\FIX.ps1 'test failure'" -ForegroundColor Gray
    Write-Host "  .\FIX.ps1 'import error'" -ForegroundColor Gray
    Write-Host "  .\FIX.ps1 'syntax error'" -ForegroundColor Gray
    Write-Host ""
    $Issue = Read-Host "Describe the issue"
}

if (-not [string]::IsNullOrEmpty($Issue)) {
    Write-Host "[FIXING] Issue: $Issue" -ForegroundColor Green
    Write-Host ""
    & .\run_psnappbot.bat --project . "Fix $Issue automatically"
    Write-Host ""
    Write-Host "[DONE] Fix attempt completed." -ForegroundColor Green
}
# setup_repo.ps1
# This script initializes a git repo including the local files and pushes to GitHub.

# Ensure we are in the script's directory
Set-Location $PSScriptRoot

$RemoteUrl = "https://github.com/cblocb/chutesladders"

# Find git executable
$GitPath = "git"
$PossiblePaths = @(
    "C:\Program Files\Git\cmd\git.exe",
    "C:\Program Files (x86)\Git\cmd\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe"
)

foreach ($path in $PossiblePaths) {
    if (Test-Path $path) {
        $GitPath = "& `"$path`""
        Write-Host "Found git at $path" -ForegroundColor Cyan
        break
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue) -and $GitPath -eq "git") {
    Write-Error "Git is not installed or not in your PATH. Please restart your terminal if you just installed it."
    exit 1
}

# Initialize repository first so config commands work
Write-Host "Initializing repository..." -ForegroundColor Cyan
Invoke-Expression "$GitPath init"
# Rename branch to main to match GitHub
Invoke-Expression "$GitPath branch -M main"

# Check and configure git identity if missing
$Email = Invoke-Expression "$GitPath config user.email"
if (-not $Email) {
    Write-Host "Git identity not set. Configuring local identity for this repository..." -ForegroundColor Yellow
    Invoke-Expression "$GitPath config user.email 'user@example.com'"
    Invoke-Expression "$GitPath config user.name 'User'"
}

Write-Host "Adding files..." -ForegroundColor Cyan
Invoke-Expression "$GitPath add ."

Write-Host "Committing..." -ForegroundColor Cyan
Invoke-Expression "$GitPath commit -m 'Initial commit of Chutes and Ladders simulation'"

# Verify commit succeeded
$CommitCheck = Invoke-Expression "$GitPath rev-parse --verify HEAD 2>&1"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Commit failed. Please check the output above."
    exit 1
}

Write-Host "Adding remote origin $RemoteUrl..." -ForegroundColor Cyan
# Check if remote exists
$Remotes = Invoke-Expression "$GitPath remote"
if ($Remotes -match "origin") {
    Invoke-Expression "$GitPath remote set-url origin $RemoteUrl"
}
else {
    Invoke-Expression "$GitPath remote add origin $RemoteUrl"
}

Write-Host "Pulling existing changes (if any) to avoid conflicts..." -ForegroundColor Cyan
# Pull with rebase 
Invoke-Expression "$GitPath pull origin main --allow-unrelated-histories --rebase"

Write-Host "Pushing to remote..." -ForegroundColor Cyan
Invoke-Expression "$GitPath push -u origin main"

Write-Host "Done!" -ForegroundColor Green

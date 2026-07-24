# install-global.ps1 — Install PM skills globally for Claude Code (Windows)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $ScriptDir
$SourceDir = Join-Path $RepoDir ".claude\commands"
$TargetDir = Join-Path $env:USERPROFILE ".claude\commands"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PM Skills for Claude Code - Global Installer" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source: $SourceDir"
Write-Host "Target: $TargetDir"
Write-Host ""

# Check source exists
if (-not (Test-Path $SourceDir)) {
    Write-Host "ERROR: Source directory not found: $SourceDir" -ForegroundColor Red
    Write-Host "Make sure you're running this from the repo root or scripts\ directory."
    exit 1
}

# Count files
$Files = Get-ChildItem -Path $SourceDir -Filter "*.md"
$FileCount = $Files.Count
Write-Host "Found $FileCount skill files to install."
Write-Host ""

# Warn about overwrites
if (Test-Path $TargetDir) {
    $Existing = (Get-ChildItem -Path $TargetDir -Filter "*.md" -ErrorAction SilentlyContinue).Count
    if ($Existing -gt 0) {
        Write-Host "WARNING: $TargetDir already contains $Existing .md files." -ForegroundColor Yellow
        Write-Host "Files with the same name will be OVERWRITTEN." -ForegroundColor Yellow
        Write-Host ""
        $Response = Read-Host "Continue? (y/N)"
        if ($Response -ne "y" -and $Response -ne "Y") {
            Write-Host "Aborted."
            exit 0
        }
    }
}

# Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# Copy files
Copy-Item -Path "$SourceDir\*.md" -Destination $TargetDir -Force

Write-Host ""
Write-Host "Done! $FileCount PM skills installed globally." -ForegroundColor Green
Write-Host ""
Write-Host "You can now use /persona, /prd, /discovery, etc. in any project."
Write-Host "Open Claude Code in any directory to start using them."

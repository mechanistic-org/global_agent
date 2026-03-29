param ()

$ErrorActionPreference = "Stop"
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " Syncing Google Workspace MCP Core Skills" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$TempDir = Join-Path $env:TEMP "gws_skills_sync"
if (Test-Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
New-Item -ItemType Directory -Path $TempDir | Out-Null

$ZipPath = Join-Path $TempDir "cli-main.zip"
$ExtractPath = Join-Path $TempDir "extracted"

Write-Host "1. Downloading latest 'cli' repository from googleworkspace..."
Invoke-WebRequest -Uri "https://github.com/googleworkspace/cli/archive/refs/heads/main.zip" -OutFile $ZipPath

Write-Host "2. Extracting archive..."
Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force

$SourceSkillsDir = Join-Path $ExtractPath "cli-main\skills"
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$TargetSkillsDir = Join-Path $RootDir ".agent\skills"

if (-not (Test-Path $SourceSkillsDir)) {
    Write-Host "ERROR: Upstream structure changed. 'skills' directory not found in zip." -ForegroundColor Red
    exit 1
}

# The whitelist: ONLY sync these core structural skills. Drop all 'recipe/persona' bloated modules.
$Allowed = @(
    "gws-calendar", "gws-calendar-agenda", "gws-calendar-insert", 
    "gws-docs", "gws-docs-write",
    "gws-drive", "gws-drive-upload",
    "gws-events", "gws-events-renew", "gws-events-subscribe",
    "gws-gmail", "gws-gmail-read", "gws-gmail-reply", "gws-gmail-reply-all", "gws-gmail-send",
    "gws-sheets", "gws-sheets-append", "gws-sheets-read"
)

Write-Host "3. Syncing whitelisted modules to $TargetSkillsDir..."
if (-Not (Test-Path $TargetSkillsDir)) {
    New-Item -ItemType Directory -Path $TargetSkillsDir | Out-Null
}

$SyncCount = 0
foreach ($skill in $Allowed) {
    $srcFolder = Join-Path $SourceSkillsDir $skill
    $dstFolder = Join-Path $TargetSkillsDir $skill
    
    if (Test-Path $srcFolder) {
        if (Test-Path $dstFolder) {
            Remove-Item -Recurse -Force $dstFolder
        }
        Copy-Item -Path $srcFolder -Destination $TargetSkillsDir -Recurse -Force
        Write-Host "   + [Synced] $skill" -ForegroundColor Green
        $SyncCount++
    } else {
        Write-Host "   ? [Missing Upstream] $skill" -ForegroundColor Yellow
    }
}

$TotalUpstream = (Get-ChildItem -Path $SourceSkillsDir -Directory).Count
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Complete. Synced $SyncCount module dependencies." -ForegroundColor Green
Write-Host "Ignored $( $TotalUpstream - $SyncCount ) upstream recipes/personas."
Write-Host "=============================================" -ForegroundColor Cyan

# Cleanup
Remove-Item -Recurse -Force $TempDir
exit 0

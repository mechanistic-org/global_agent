param (
    [Parameter(Mandatory=$true)]
    [string]$TargetIssue,

    [Parameter(Mandatory=$false)]
    [string]$TargetRepo = "mechanistic-org/global_agent"
)

$ErrorActionPreference = "Stop"

# Get absolute paths to mount
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$RegistryDir = Join-Path $RootDir "registry"
$OutputDir = Join-Path $RootDir "output"
$EnvFile = Join-Path $RootDir ".env"

if (-Not (Test-Path $EnvFile)) {
    Write-Host "CRITICAL: .env file not found at $EnvFile" -ForegroundColor Red
    exit 1
}

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " IGNITING NANOCLAW CONTAINER" -ForegroundColor Cyan
Write-Host " Target Issue : $TargetIssue"
Write-Host " Target Repo  : $TargetRepo"
Write-Host "===============================================" -ForegroundColor Cyan

# Remove network host requirement and explicitly inject ROUTER_SSE_URL for Docker Desktop bridging
docker run --rm `
  --env-file $EnvFile `
  -e TARGET_ISSUE=$TargetIssue `
  -e TARGET_REPO=$TargetRepo `
  -e ROUTER_SSE_URL="http://host.docker.internal:8000/sse" `
  -v "${RegistryDir}:/registry" `
  -v "${OutputDir}:/output" `
  nanoclaw:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "NanoClaw execution completed successfully." -ForegroundColor Green
} else {
    Write-Host "NanoClaw execution failed with code $LASTEXITCODE." -ForegroundColor Red
}

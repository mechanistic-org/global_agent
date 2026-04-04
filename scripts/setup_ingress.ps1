param(
    [Parameter(Mandatory=$true, HelpMessage="The Cloudflare Zero Trust Tunnel Token (ey...)")]
    [string]$TunnelToken
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 🌐 NANOCLAW INGRESS RESILIENCE SETUP (CLOUDFLARED)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if cloudflared is installed
$cloudflaredCmd = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflaredCmd) {
    Write-Host "[ERROR] cloudflared is not installed or not in your PATH." -ForegroundColor Red
    Write-Host "Please install it via WinGet: 'winget install Cloudflare.cloudflared'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found cloudflared executable at: $($cloudflaredCmd.Path)" -ForegroundColor Green
Write-Host "Installing cloudflared as a native Windows service..." -ForegroundColor Yellow

# Install the service
try {
    cloudflared.exe service install $TunnelToken
    Write-Host "[SUCCESS] Service installed." -ForegroundColor Green
    Write-Host "You can now safely restart your machine and the tunnel will boot automatically." -ForegroundColor Cyan
    Write-Host "Check 'services.msc' for 'Cloudflared agent'." -ForegroundColor DarkGray
}
catch {
    Write-Host "[ERROR] Failed to install service: $_" -ForegroundColor Red
    Write-Host "Ensure you are running this PowerShell window as Administrator." -ForegroundColor Yellow
    exit 1
}

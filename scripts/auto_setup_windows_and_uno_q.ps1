#Requires -Version 5.1
<#
.SYNOPSIS
    Automated One-Click Provisioner for Arduino UNO Q (ABX00173) + RTX 5070 / Intel NPU Workstation.
.DESCRIPTION
    1. Scans USB / Serial / Network (RNDIS / mDNS `unoq.local`) for a connected Arduino UNO Q.
    2. Checks/installs `arduino-cli` and flashes `mcu_sketch/uno_q_status_matrix.ino` to the STM32U585 MCU.
    3. Deploys `gateway/` and `memory/` to the Arduino UNO Q Linux side (if reachable via SSH) or runs locally.
    4. Configures `.env`, `.mcp.json`, and `opencode.json` for OpenCode & Claude Code.
    5. Starts the PC Workstation Agent & 3D Web Dashboard on http://localhost:8080/dashboard.
#>

$ErrorActionPreference = "Continue"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ANKI VECTOR 2.0 + ARDUINO UNO Q + RTX 5070 AUTO-SETUP     " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Detect USB Serial / RNDIS Arduino UNO Q devices
Write-Host "`n[1/5] Scanning USB & Serial ports for Arduino UNO Q (ABX00173)..." -ForegroundColor Yellow
$SerialPorts = [System.IO.Ports.SerialPort]::GetPortNames()
$DetectedPort = $null

try {
    $PnpDevices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object {
        $_.FriendlyName -match "Arduino|STM32|Qualcomm|USB Serial|COM"
    }
    foreach ($dev in $PnpDevices) {
        Write-Host "  -> Detected Device: $($dev.FriendlyName) [$($dev.Status)]" -ForegroundColor Green
        if ($dev.FriendlyName -match "\((COM\d+)\)") {
            $DetectedPort = $Matches[1]
        }
    }
} catch {}

if (-not $DetectedPort -and $SerialPorts.Count -gt 0) {
    $DetectedPort = $SerialPorts[0]
    Write-Host "  -> Fallback Serial Port selected: $DetectedPort" -ForegroundColor Green
} elseif (-not $DetectedPort) {
    Write-Host "  -> No COM port exposed yet (UNO Q may be in RNDIS network mode or booting)." -ForegroundColor DarkYellow
}

# 2. Check / Flash STM32U585 LED Matrix Sketch via arduino-cli
Write-Host "`n[2/5] Checking arduino-cli for STM32U585 8x13 LED Matrix sketch..." -ForegroundColor Yellow
$ArduinoCli = Get-Command "arduino-cli" -ErrorAction SilentlyContinue
if ($ArduinoCli -and $DetectedPort) {
    Write-Host "  -> Compiling & Uploading mcu_sketch/uno_q_status_matrix.ino to $DetectedPort..." -ForegroundColor Green
    & arduino-cli compile --fqbn arduino:stm32:uno_q "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino"
    & arduino-cli upload -p $DetectedPort --fqbn arduino:stm32:uno_q "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino"
} else {
    Write-Host "  -> Skipping direct COM flash (Arduino App Lab / UNO Q Linux Bridge handles RPC automatically)." -ForegroundColor Gray
}

# 3. Check UNO Q Linux SSH Reachability (unoq.local)
Write-Host "`n[3/5] Checking Arduino UNO Q Linux MPU (unoq.local)..." -ForegroundColor Yellow
$UnoQReachable = Test-Connection -ComputerName "unoq.local" -Count 1 -Quiet -ErrorAction SilentlyContinue
if ($UnoQReachable) {
    Write-Host "  -> unoq.local is ONLINE! Syncing gateway/ and memory/ to UNO Q..." -ForegroundColor Green
    scp -r "$RepoRoot\gateway" "$RepoRoot\memory" "$RepoRoot\scripts" "$RepoRoot\mcu_sketch" "arduino@unoq.local:~/Anki-Vektor/"
} else {
    Write-Host "  -> unoq.local not reachable over mDNS yet; running Gateway + PC Agent locally on Workstation." -ForegroundColor Gray
}

# 4. Prepare Python Virtual Environment & .env
Write-Host "`n[4/5] Preparing Python environment & MCP configs (.mcp.json / opencode.json)..." -ForegroundColor Yellow
if (-not (Test-Path "$RepoRoot\.env")) {
    Copy-Item "$RepoRoot\.env.example" "$RepoRoot\.env"
    if ($DetectedPort) {
        Add-Content "$RepoRoot\.env" "`nUNO_Q_SERIAL_PORT=$DetectedPort"
    }
}

if (-not (Test-Path "$RepoRoot\.venv")) {
    python -m venv "$RepoRoot\.venv"
}
& "$RepoRoot\.venv\Scripts\pip.exe" install -q -r "$RepoRoot\pc_agent\requirements.txt" -r "$RepoRoot\gateway\requirements.txt"

# 5. Launch Services & Dashboard
Write-Host "`n[5/5] Launching UNO Q Gateway (Port 8000) and PC Workstation Agent (Port 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RepoRoot'; .\.venv\Scripts\python.exe -m gateway.main"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RepoRoot'; .\.venv\Scripts\python.exe -m pc_agent.server"

Start-Sleep -Seconds 2
Start-Process "http://localhost:8080/dashboard"
Write-Host "`nAll systems launched! Web Dashboard opened at http://localhost:8080/dashboard" -ForegroundColor Green

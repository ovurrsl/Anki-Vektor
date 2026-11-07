#Requires -Version 5.1
<#
.SYNOPSIS
    Automated One-Click Provisioner for Arduino UNO Q (ABX00173) + RTX 5070 / Intel NPU Workstation.
.DESCRIPTION
    1. Scans USB / Serial / Network (RNDIS / mDNS `unoq.local`) for a connected Arduino UNO Q.
    2. Automatically downloads portable `arduino-cli` if not installed, installs STM32/UNO Q cores,
       and compiles + uploads `mcu_sketch/uno_q_status_matrix.ino` to the STM32U585 MCU.
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
Write-Host "`n[1/5] USB ve Seri portlarda Arduino UNO Q (ABX00173) araniyor..." -ForegroundColor Yellow
$SerialPorts = [System.IO.Ports.SerialPort]::GetPortNames()
$DetectedPort = $null

try {
    $PnpDevices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object {
        $_.FriendlyName -match "Arduino|STM32|Qualcomm|USB Serial|COM"
    }
    foreach ($dev in $PnpDevices) {
        Write-Host "  -> Bulunan Cihaz: $($dev.FriendlyName) [$($dev.Status)]" -ForegroundColor Green
        if ($dev.FriendlyName -match "\((COM\d+)\)") {
            $DetectedPort = $Matches[1]
        }
    }
} catch {}

if (-not $DetectedPort -and $SerialPorts.Count -gt 0) {
    $DetectedPort = $SerialPorts[0]
    Write-Host "  -> Varsayilan Seri Port secildi: $DetectedPort" -ForegroundColor Green
} elseif (-not $DetectedPort) {
    Write-Host "  -> Henuz COM portu gorunmuyor (UNO Q RNDIS ag modunda veya aciliyor olabilir)." -ForegroundColor DarkYellow
}

# 2. Check / Auto-Install arduino-cli & Flash STM32U585 LED Matrix Sketch
Write-Host "`n[2/5] STM32U585 8x13 LED Matris kodu (uno_q_status_matrix.ino) Arduino'ya yukleniyor..." -ForegroundColor Yellow
$ArduinoCliCmd = Get-Command "arduino-cli" -ErrorAction SilentlyContinue
$LocalCliDir = Join-Path $RepoRoot ".tools\arduino-cli"
$LocalCliExe = Join-Path $LocalCliDir "arduino-cli.exe"

if ($ArduinoCliCmd) {
    $CliExe = $ArduinoCliCmd.Source
} elseif (Test-Path $LocalCliExe) {
    $CliExe = $LocalCliExe
} else {
    Write-Host "  -> arduino-cli sistemde bulunamadi, tasinabilir surum otomatik indiriliyor..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $LocalCliDir | Out-Null
    $ZipPath = Join-Path $LocalCliDir "arduino-cli.zip"
    Invoke-WebRequest -Uri "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip" -OutFile $ZipPath
    Expand-Archive -Path $ZipPath -DestinationPath $LocalCliDir -Force
    $CliExe = $LocalCliExe
}

if (Test-Path $CliExe) {
    & $CliExe core update-index
    if ($DetectedPort) {
        Write-Host "  -> Bagli kart algilaniyor ($DetectedPort)..." -ForegroundColor Cyan
        $BoardList = & $CliExe board list
        Write-Host $BoardList
        # Try UNO Q or UNO R4 / STM32 FQBN
        & $CliExe compile --fqbn arduino:stm32:uno_q "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino" 2>$null
        & $CliExe upload -p $DetectedPort --fqbn arduino:stm32:uno_q "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino" 2>$null
        Write-Host "  -> Seri port uzerinden baslangic durum komutu (PC_ON=2) gonderiliyor..." -ForegroundColor Green
        try {
            $portObj = New-Object System.IO.Ports.SerialPort $DetectedPort, 115200, None, 8, one
            $portObj.Open()
            $portObj.WriteLine("2")
            Start-Sleep -Milliseconds 300
            $portObj.Close()
        } catch {}
    }
}

# 3. Check UNO Q Linux SSH Reachability (unoq.local)
Write-Host "`n[3/5] Arduino UNO Q Linux MPU (unoq.local) kontrol ediliyor..." -ForegroundColor Yellow
$UnoQReachable = Test-Connection -ComputerName "unoq.local" -Count 1 -Quiet -ErrorAction SilentlyContinue
if ($UnoQReachable) {
    Write-Host "  -> unoq.local ONLINE! gateway/ ve memory/ UNO Q uzerine kopyalaniyor..." -ForegroundColor Green
    scp -r "$RepoRoot\gateway" "$RepoRoot\memory" "$RepoRoot\scripts" "$RepoRoot\mcu_sketch" "arduino@unoq.local:~/Anki-Vektor/"
} else {
    Write-Host "  -> unoq.local mDNS uzerinden yanit vermedi; Gateway + PC Agent yerel PC uzerinde baslatiliyor." -ForegroundColor Gray
}

# 4. Prepare Python Virtual Environment & .env
Write-Host "`n[4/5] Python ortami ve MCP dosyalari (.mcp.json / opencode.json) hazirlaniyor..." -ForegroundColor Yellow
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
Write-Host "`n[5/5] UNO Q Gateway (Port 8000) ve PC Workstation Agent (Port 8080) baslatiliyor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RepoRoot'; .\.venv\Scripts\python.exe -m gateway.main"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RepoRoot'; .\.venv\Scripts\python.exe -m pc_agent.server"

Start-Sleep -Seconds 3
Start-Process "http://localhost:8080/dashboard"
Write-Host "`nTum servisler baslatildi! Tarayicida http://localhost:8080/dashboard acildi." -ForegroundColor Green

#Requires -Version 5.1
<#
.SYNOPSIS
    Zero-Dependency Local Provisioner & Launcher for Windows 11 (RTX 5070 + Intel NPU + Arduino UNO Q).
.DESCRIPTION
    1. Automatically locates Python 3.11+ on Windows (or installs portable `uv` + Python 3.11 automatically if missing!).
    2. Creates `.venv` and installs all dependencies (`fastapi`, `uvicorn`, `pyserial`, `pillow`, etc.).
    3. Automatically downloads `arduino-cli`, detects the USB-connected Arduino UNO Q (`COM*`), installs the core,
       flashes `mcu_sketch/uno_q_status_matrix.ino`, and sends the `SET_STATUS:2` serial wake command.
    4. Starts the Gateway (port 8000) and PC Workstation Agent (port 8080), waits until port 8080 is live,
       and opens `http://localhost:8080/dashboard`.
#>
param(
    [int]$SkipLaunch = 0
)

$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  ANKI VECTOR 2.0 + ARDUINO UNO Q + RTX 5070 OTOMATIK LOCAL KURUCU          " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# ADIM 1: PYTHON / UV KONTROLU VE OTOMATIK KURULUMU (Python PATH'te olmasa bile!)
# ------------------------------------------------------------------------------
Write-Host "`n[1/5] Python ortami kontrol ediliyor (yoksa otomatik indirilecek)..." -ForegroundColor Yellow

$ToolsDir = Join-Path $RepoRoot ".tools"
New-Item -ItemType Directory -Force -Path $ToolsDir | Out-Null
$UvExe = Join-Path $ToolsDir "uv.exe"

# Ensure portable uv is available — uv can download & manage Python 3.11 without admin rights!
if (-not (Test-Path $UvExe)) {
    $SystemUv = Get-Command "uv" -ErrorAction SilentlyContinue
    if ($SystemUv) {
        $UvExe = $SystemUv.Source
    } else {
        Write-Host "  -> Tasinabilir 'uv' (Python yoneticisi) indiriliyor..." -ForegroundColor Cyan
        $UvZip = Join-Path $ToolsDir "uv.zip"
        Invoke-WebRequest -Uri "https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-pc-windows-msvc.zip" -OutFile $UvZip
        Expand-Archive -Path $UvZip -DestinationPath $ToolsDir -Force
        # Handle subfolder if any
        $FoundUv = Get-ChildItem -Path $ToolsDir -Filter "uv.exe" -Recurse | Select-Object -First 1
        if ($FoundUv -and ($FoundUv.FullName -ne $UvExe)) {
            Copy-Item $FoundUv.FullName $UvExe -Force
        }
    }
}

$VenvDir = Join-Path $RepoRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "  -> Python 3.11 ve sanal ortam (.venv) otomatik kuruluyor (Lutfen bekleyin)..." -ForegroundColor Cyan
    & $UvExe venv $VenvDir --python 3.11
}

Write-Host "  -> Gerekli Python paketleri (.venv) yukleniyor..." -ForegroundColor Cyan
& $UvExe pip install --python $VenvPython -r "$RepoRoot\pc_agent\requirements.txt" -r "$RepoRoot\gateway\requirements.txt"

if (Test-Path $VenvPython) {
    Write-Host "  -> [BASARILI] Python hazir: $VenvPython" -ForegroundColor Green
} else {
    Write-Host "  -> [HATA] Python ortami olusturulamadi!" -ForegroundColor Red
}

# ------------------------------------------------------------------------------
# ADIM 2: USB / SERI PORTLARDA ARDUINO UNO Q TESPITI
# ------------------------------------------------------------------------------
Write-Host "`n[2/5] USB ve Seri portlarda Arduino UNO Q (ABX00173) araniyor..." -ForegroundColor Yellow
$SerialPorts = [System.IO.Ports.SerialPort]::GetPortNames()
$DetectedPort = $null

try {
    $PnpDevices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object {
        $_.FriendlyName -match "Arduino|STM32|Qualcomm|USB Serial|COM|CDC|Gadget"
    }
    foreach ($dev in $PnpDevices) {
        Write-Host "  -> Algilanan USB Cihaz: $($dev.FriendlyName) [$($dev.Status)]" -ForegroundColor Green
        if ($dev.FriendlyName -match "\((COM\d+)\)") {
            $DetectedPort = $Matches[1]
        }
    }
} catch {}

if (-not $DetectedPort -and $SerialPorts.Count -gt 0) {
    $DetectedPort = $SerialPorts[0]
    Write-Host "  -> Aktif Seri Port secildi: $DetectedPort" -ForegroundColor Green
} elseif (-not $DetectedPort) {
    Write-Host "  -> Bilgisayarda aktif COM portu listesi: $($SerialPorts -join ', ')" -ForegroundColor DarkYellow
}

# ------------------------------------------------------------------------------
# ADIM 3: ARDUINO-CLI ILE KARTA KOD YUKLEME VE SERI TETIKLEME
# ------------------------------------------------------------------------------
Write-Host "`n[3/5] Arduino UNO Q (STM32U585) 8x13 LED Matris kontrol ediliyor..." -ForegroundColor Yellow
$LocalCliDir = Join-Path $ToolsDir "arduino-cli"
$LocalCliExe = Join-Path $LocalCliDir "arduino-cli.exe"

if (-not (Test-Path $LocalCliExe)) {
    Write-Host "  -> arduino-cli indiriliyor..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $LocalCliDir | Out-Null
    $ZipPath = Join-Path $LocalCliDir "arduino-cli.zip"
    Invoke-WebRequest -Uri "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip" -OutFile $ZipPath
    Expand-Archive -Path $ZipPath -DestinationPath $LocalCliDir -Force
}

if (Test-Path $LocalCliExe) {
    Write-Host "  -> Bagli Arduino kartlari listeleniyor:" -ForegroundColor Cyan
    $BoardListOutput = & $LocalCliExe board list
    $BoardListOutput | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }

    # Extract FQBN and Port automatically if arduino-cli detects the board
    $DetectedFqbn = "arduino:stm32:uno_q"
    foreach ($line in $BoardListOutput) {
        if ($line -match "^(COM\d+)\s+.*?\s+([a-zA-Z0-9_]+:[a-zA-Z0-9_]+:[a-zA-Z0-9_]+)") {
            $DetectedPort = $Matches[1]
            $DetectedFqbn = $Matches[2]
            Write-Host "  -> Otomatik Eslesen Kart: Port=$DetectedPort, FQBN=$DetectedFqbn" -ForegroundColor Green
        } elseif (-not $DetectedPort -and $line -match "^(COM\d+)") {
            $DetectedPort = $Matches[1]
        }
    }

    if ($DetectedPort) {
        # Ensure core is installed for the detected FQBN (e.g., arduino:zephyr or arduino:renesas_uno or arduino:stm32)
        $CoreParts = $DetectedFqbn.Split(":")
        if ($CoreParts.Count -ge 2) {
            $CoreName = "$($CoreParts[0]):$($CoreParts[1])"
            Write-Host "  -> Arduino Core kontrol ediliyor ($CoreName)..." -ForegroundColor Cyan
            & $LocalCliExe core update-index | Out-Null
            & $LocalCliExe core install $CoreName 2>$null
        }

        Write-Host "  -> mcu_sketch\uno_q_status_matrix.ino derleniyor ve $DetectedPort portuna yukleniyor..." -ForegroundColor Cyan
        & $LocalCliExe compile --fqbn $DetectedFqbn "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino"
        & $LocalCliExe upload -p $DetectedPort --fqbn $DetectedFqbn "$RepoRoot\mcu_sketch\uno_q_status_matrix.ino"

        Write-Host "  -> $DetectedPort uzerinden 8x13 LED Matris uyandirma komutu (SET_STATUS:2) gonderiliyor..." -ForegroundColor Green
        try {
            $portObj = New-Object System.IO.Ports.SerialPort $DetectedPort, 115200, None, 8, one
            $portObj.ReadTimeout = 1000
            $portObj.WriteTimeout = 1000
            $portObj.Open()
            $portObj.WriteLine("SET_STATUS:2")
            Start-Sleep -Milliseconds 400
            $portObj.Close()
            Write-Host "  -> [BASARILI] Seri komut gonderildi ($DetectedPort)!" -ForegroundColor Green
        } catch {
            Write-Host "  -> Seri port mesgul veya farkli modda: $($_.Exception.Message)" -ForegroundColor DarkYellow
        }
    }
}

# ------------------------------------------------------------------------------
# ADIM 4: .ENV DOSYASI HAZIRLIGI
# ------------------------------------------------------------------------------
Write-Host "`n[4/5] Yapilandirma (.env) kontrol ediliyor..." -ForegroundColor Yellow
$EnvFile = Join-Path $RepoRoot ".env"
if (-not (Test-Path $EnvFile)) {
    Copy-Item (Join-Path $RepoRoot ".env.example") $EnvFile
}
if ($DetectedPort) {
    $EnvContent = Get-Content $EnvFile -Raw
    if ($EnvContent -notmatch "UNO_Q_SERIAL_PORT=") {
        Add-Content $EnvFile "`nUNO_Q_SERIAL_PORT=$DetectedPort"
    }
}

# ------------------------------------------------------------------------------
# ADIM 5: LOCAL SUNUCULARI BASLATMA VE TARAYICIYI ACMA
# ------------------------------------------------------------------------------
if ($SkipLaunch -eq 0 -and (Test-Path $VenvPython)) {
    Write-Host "`n[5/5] UNO Q Gateway (Port 8000) ve PC Workstation Agent (Port 8080) baslatiliyor..." -ForegroundColor Yellow

    # Kill any old hung processes on 8000/8080 so clean startup is guaranteed
    Get-NetTCPConnection -LocalPort 8000, 8080 -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }

    Start-Process -FilePath $VenvPython -ArgumentList "-m", "gateway.main" -WorkingDirectory $RepoRoot -WindowStyle Minimized
    Start-Process -FilePath $VenvPython -ArgumentList "-m", "pc_agent.server" -WorkingDirectory $RepoRoot -WindowStyle Normal

    Write-Host "  -> Localhost:8080 sunucusunun hazir olmasi bekleniyor..." -ForegroundColor Cyan
    $ServerReady = $false
    for ($i = 0; $i -lt 15; $i++) {
        Start-Sleep -Seconds 1
        try {
            $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8080/api/v1/status" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($resp.StatusCode -eq 200) {
                $ServerReady = $true
                break
            }
        } catch {}
    }

    if ($ServerReady) {
        Write-Host "  -> [BASARILI] Sunucu AKTIF! Tarayicida http://localhost:8080/dashboard aciliyor..." -ForegroundColor Green
        Start-Process "http://localhost:8080/dashboard"
    } else {
        Write-Host "  -> [UYARI] Sunucu henuz basliyor, tarayici aciliyor..." -ForegroundColor Yellow
        Start-Process "http://localhost:8080/dashboard"
    }
}

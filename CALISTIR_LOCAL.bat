@echo off
chcp 65001 >nul
title Anki Vector 2.0 + Arduino UNO Q + RTX 5070 Local Gelistirme ve Kontrol Merkezi
cd /d "%~dp0"

echo ============================================================================
echo   ANKI VECTOR 2.0 + ARDUINO UNO Q + RTX 5070 LOCAL CALISTIRICI (WINDOWS)
echo ============================================================================
echo.

echo [1/4] GitHub (ovurrsl/Anki-Vektor) uzerinden en guncel kodlar cekiliyor...
git pull origin main
echo.

echo [2/4] Python sanal ortami (.venv) ve paketler (pyserial, fastapi, vb.) kontrol ediliyor...
IF NOT EXIST ".venv\Scripts\python.exe" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip
pip install --quiet -r pc_agent\requirements.txt -r gateway\requirements.txt
IF NOT EXIST ".env" (
    copy .env.example .env >nul
)
echo.

echo [3/4] Bagli Arduino UNO Q (COM Port) taraniyor ve STM32U585 LED kodu kontrol ediliyor...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\auto_setup_windows_and_uno_q.ps1" -LaunchOnly:$false
echo.

echo [4/4] Local Sunucular ve Web Dashboard (http://localhost:8080/dashboard) aciliyor...
start "UNO Q Gateway (Port 8000)" cmd /k "call .venv\Scripts\activate.bat && python -m gateway.main"
start "PC Workstation Agent (Port 8080)" cmd /k "call .venv\Scripts\activate.bat && python -m pc_agent.server"

timeout /t 3 >nul
start http://localhost:8080/dashboard

echo.
echo ============================================================================
echo   TAMAMLANDI! Tarayicinizda http://localhost:8080/dashboard acildi.
echo   Gelecekte yeni guncellemeleri almak icin sadece bu dosyaya cift tiklayin!
echo ============================================================================
pause

@echo off
chcp 65001 >nul
title Anki Vector 2.0 + Arduino UNO Q + RTX 5070 Local Gelistirme ve Kontrol Merkezi
cd /d "%~dp0"

echo ============================================================================
echo   ANKI VECTOR 2.0 + ARDUINO UNO Q + RTX 5070 LOCAL CALISTIRICI (WINDOWS)
echo ============================================================================
echo.

echo [ADIM 1] GitHub (ovurrsl/Anki-Vektor) uzerinden en guncel kodlar cekiliyor...
git pull origin main
echo.

echo [ADIM 2] Otomatik Python 3.11 + Arduino UNO Q + Localhost:8080 Kurucu baslatiliyor...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\auto_setup_windows_and_uno_q.ps1"

echo.
echo ============================================================================
echo   ISLEM TAMAMLANDI!
echo   Tarayicinizda http://localhost:8080/dashboard acildi.
echo ============================================================================
pause

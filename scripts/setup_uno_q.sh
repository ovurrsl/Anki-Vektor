#!/usr/bin/env bash
# ==============================================================================
# Arduino UNO Q 4GB (ABX00173) - Headless Edge Gateway Setup Script
# Configures Debian Trixie for optimal 24/7 low-power performance.
# ==============================================================================

set -e

echo "=== [1/6] Headless Moda Geçiş (RAM Tasarrufu ~600MB) ==="
sudo systemctl set-default multi-user.target
sudo systemctl stop lightdm gdm3 sddm 2>/dev/null || true
sudo systemctl disable lightdm gdm3 sddm 2>/dev/null || true

echo "=== [2/6] Zaman Dilimi ve mDNS (unoq.local) Ayarı ==="
sudo timedatectl set-timezone Europe/Istanbul
sudo timedatectl set-ntp true

echo "=== [3/6] Temel Paketlerin Kurulumu ==="
sudo apt update
sudo apt install -y \
    build-essential \
    curl \
    git \
    pkg-config \
    libssl-dev \
    libasound2-dev \
    alsa-utils \
    wakeonlan \
    avahi-daemon \
    python3-full \
    python3-pip \
    python3-venv

sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon

# Wi-Fi güç tasarrufunu kapat (bağlantı kopmasını önler)
sudo iw dev wlan0 set power_save off 2>/dev/null || true

echo "=== [4/6] 'uv' Paket Yöneticisinin Kurulumu ==="
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "=== [5/6] Proje Dizininin Hazırlanması ==="
sudo mkdir -p /opt/vector-gateway
sudo chown -R $USER:$USER /opt/vector-gateway

cd /opt/vector-gateway
if [ ! -d ".venv" ]; then
    uv venv .venv
fi
source .venv/bin/activate
uv pip install -r requirements.txt

echo "=== [6/6] Kurulum Tamamlandı! ==="
echo "Sistemi yeniden başlatmak için: sudo reboot"

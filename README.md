# Anki Vector 2.0 & Embodied AI Hibrit Mimarisi

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Standard-purple.svg)](https://modelcontextprotocol.io/)
[![Hardware](https://img.shields.io/badge/Hardware-Arduino_UNO_Q_|_RTX_5070_|_Intel_NPU-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-20%20Passed-brightgreen.svg)]()

Bu depo; **Anki Vector 2.0** (fiziksel robotik beden), **Arduino UNO Q 4GB** (7/24 açık nöbetçi uç ağ geçidi), **Masaüstü PC (NVIDIA GeForce RTX 5070 + Intel Core Ultra NPU 3)** ve **Google Gemini Pro Live API** katmanlarını birleştiren üç katmanlı Bedenlenmiş Yapay Zeka (Embodied AI) mimarisinin resmi monorepo kaynak kodlarını içerir.

---

## 📌 Mimari Genel Bakış

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                              BULUT KATMANI                             │
 │  - Google AI Studio (Gemini Pro Live API - WebSocket Audio/Vision)     │
 │  - Google Search Grounding (Canlı Web Doğrulaması)                     │
 └───────────────────────────────────▲────────────────────────────────────┘
                                     │ (Trafik & Bilgi)
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │               ARDUINO UNO Q 4GB (ABX00173 - 7/24 Nöbetçi)              │
 │  - Headless Debian Trixie + Harici Beslemeli Type-C Hub (5V/3A)        │
 │  - wirepod-vector-sdk (Yerel gRPC / sdk_config.ini)                    │
 │  - sqlite-vec (Kalıcı Epizodik & Olgusal Hafıza - vec0 Sanal Tablosu)  │
 │  - Wake-on-LAN (UDP Port 9 / WoL Daemon) & Ping Sentinel               │
 │  - Half-Duplex AEC (Vector konuşurken USB mikrofona Mute + 400ms tail) │
 │  - soxr / rubato (24 kHz Gemini PCM -> 16 kHz Vector WAV Dönüşümü)     │
 │  - STM32U585 MCU (8x13 Mavi LED Matrisinde Durum Göstergesi)           │
 └─────────────▲───────────────────────────────▲──────────────────────────┘
               │                               │
        (Wi-Fi gRPC)                     (LAN / FastMCP HTTP/SSE)
               │                               │
 ┌─────────────▼───────────────┐ ┌─────────────▼──────────────────────────┐
 │      ANKI VECTOR 2.0        │ │        RTX 5070 + INTEL NPU PC         │
 │  - Qualcomm Snapdragon 212  │ │  - RTX 5070 (12GB GDDR7 Blackwell):    │
 │  - 600 mAh LiPo (~52 dk)    │ │      * Qwen 2.5 14B Q4_K_M (Abliter)   │
 │  - 16 kHz Mono Hoparlör     │ │      * Coqui XTTS-v2 / F5-TTS          │
 │  - ToF / Uçurum Sensörleri  │ │  - Intel NPU 3 (Arrow Lake 13 TOPS):   │
 │  - 184x96 Renkli IPS LCD    │ │      * Whisper Large-v3 Turbo (INT8)   │
 │  - Docked vs Roaming Modu   │ │      * YOLOv8n (Statik [1,3,640,640])  │
 └─────────────────────────────┘ │  - Insta360 Link 2 (USB 3.2):           │
                                 │      * Arcseconds PTZ (Step=3600)      │
                                 │      * DeskView (-80° = -288000 arcsec)│
                                 │  - Claude Code CLI & Web Dashboard     │
                                 └────────────────────────────────────────┘
```

---

## 🚀 Donanım Simülasyonu (Mock Katmanı)

Robot ve Insta360 kameranız henüz elinizde olmasa bile mimariyi **hemen bugün test edebilirsiniz**:
* `MOCK_ROBOT=True`: Vector'ün hareket fiziğini, kafa/kol motor açılarını, bataryasını, ses çalmasını ve göz ekranını bellek içinde birebir simüle eder.
* `MOCK_CAMERA=True`: Insta360 Link 2'nin motor açılarını takip eder ve masayı kuşbakışı gösteren dinamik 1280x720 sentetik JPEG görüntüsü üretir.
* **Fiziksel donanım geldiğinde:** `.env` dosyasında `MOCK_ROBOT=False` ve `MOCK_CAMERA=False` yapmanız yeterlidir; hiçbir kod değişikliği gerekmez!

---

## 📂 Dizin Yapısı

```text
Anki-Vektor/
├── gateway/                 # Arduino UNO Q 7/24 Nöbetçi Ağ Geçidi
│   ├── config.py            # Ortam değişkenleri ve ayarlar
│   ├── main.py              # Asyncio ana olay döngüsü ve FastAPI REST servisi
│   ├── vector_bridge.py     # wirepod-vector-sdk & MockVectorRobot köprüsü
│   ├── audio_pipeline.py    # Half-Duplex AEC & 24k->16k ses resampler
│   ├── wol_sentinel.py      # Wake-on-LAN sihirli paket fırlatıcı ve ping takipçisi
│   ├── intent_parser.py     # Çevrimdışı Türkçe niyet çözümleyici
│   └── requirements.txt     # UNO Q hafif paket listesi
├── pc_agent/                # RTX 5070 + Intel NPU Masaüstü PC Ajanı
│   ├── config.py            # PC ayarları
│   ├── server.py            # FastAPI sunucusu, REST API & Web Dashboard
│   ├── camera_ptz.py        # Insta360 Link 2 arcseconds PTZ & MockCamera
│   ├── npu_engine.py        # Intel NPU OpenVINO Whisper & YOLO entegrasyonu
│   ├── llm_router.py        # Gemini Live API, Yerel Qwen LLM ve Claude Code köprüsü
│   ├── templates/
│   │   └── dashboard.html   # Canlı gösterge paneli (Web UI)
│   └── requirements.txt     # PC bağımlılıkları
├── brain_mcp/               # Model Context Protocol (FastMCP) Standart Araç Seti
│   ├── tools.py             # VectorClaw uyumlu robot ve sistem araçları
│   └── server.py            # FastMCP stdio ve SSE sunucusu
├── memory/                  # sqlite-vec Kalıcı Epizodik Hafıza Katmanı
│   ├── db.py                # vec0 sanal tablo motoru ve benzerlik araması
│   └── schema.sql           # Vektör ve ilişkisel hafıza şeması
├── mcu_sketch/              # Arduino UNO Q STM32U585 Kodu
│   └── uno_q_status_matrix.ino # 8x13 Mavi LED matris durum ekranı ve Bridge RPC
├── tests/                   # Kapsamlı Otomatik Test Paketi (20 test)
│   ├── test_gateway.py      # WoL, ses resampler ve intent parser testleri
│   ├── test_vector_mock.py  # Mock Vector hareket ve sensör testleri
│   ├── test_camera_ptz.py   # Arcseconds PTZ ve Mock kamera testleri
│   ├── test_memory.py       # sqlite-vec hafıza okuma/yazma testleri
│   ├── test_mcp_tools.py    # FastMCP araç çağrı testleri
│   └── test_pc_agent.py     # PC Agent REST uç noktaları ve dashboard testi
├── scripts/                 # Kurulum ve Çalıştırma Betikleri
│   ├── setup_uno_q.sh       # Headless Debian kurulum betiği
│   ├── run_gateway.sh       # Gateway başlatıcı (Linux)
│   ├── run_pc_agent.bat     # PC Ajanı başlatıcı (Windows 11)
│   └── run_pc_agent.sh      # PC Ajanı başlatıcı (Linux/WSL)
├── systemd/                 # Arka Plan Servis Tanımı
│   └── vector-gateway.service
├── .env.example             # Konfigürasyon şablonu
└── README.md                # Proje dokümantasyonu
```

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Hızlı Başlangıç (Geliştirme & Test Ortamı)

```bash
# Depoyu klonlayın
git clone https://github.com/ovurrsl/Anki-Vektor.git
cd Anki-Vektor

# uv ile sanal ortam oluşturun ve bağımlılıkları yükleyin
uv venv .venv
source .venv/bin/activate  # Windows için: .venv\Scripts\activate
uv pip install -r gateway/requirements.txt -r pc_agent/requirements.txt pytest pytest-asyncio

# Konfigürasyonu hazırlayın
cp .env.example .env
```

### 2. Otomatik Testleri Çalıştırma

Tüm modüllerin kararlılığını doğrulamak için:
```bash
pytest -v tests/
```
*(20 birim ve entegrasyon testinin tamamı başarıyla geçecektir.)*

### 3. PC Ajanı ve Web Dashboard'u Başlatma

**Windows 11 üzerinde:**
```cmd
scripts\run_pc_agent.bat
```

**Linux / WSL üzerinde:**
```bash
chmod +x scripts/*.sh
./scripts/run_pc_agent.sh
```

Tarayıcınızı açın ve gösterge paneline gidin:
👉 **`http://localhost:8080/dashboard`**

Bu ekrandan:
* Sanal Vector'ü ileri/geri sürebilir, baş/kol açılarını değiştirebilir, göz ifadelerini seçebilirsiniz.
* Insta360 kamerasını Pan/Tilt kaydırıcılarıyla döndürebilir veya **Masa Modu (DeskView)** ile masaya 90° eğebilirsiniz.
* Canlı yapay zeka sohbetiyle Vector ile Türkçe konuşabilirsiniz.

### 4. Arduino UNO Q Gateway'i Başlatma

```bash
./scripts/run_gateway.sh
```
Gateway `http://0.0.0.0:8000` portunda açılır; Wake-on-LAN nöbetçisi ve Half-Duplex ses hattı 7/24 kesintisiz çalışır.

---

## 🤖 Model Context Protocol (FastMCP) Entegrasyonu

Proje, **Claude Code CLI** veya **Gemini CLI** ile doğrudan konuşabilen bir MCP sunucusu içerir.

Claude Code'a Vector araçlarını eklemek için:
```bash
claude mcp add vector python /path/to/Anki-Vektor/brain_mcp/server.py
```

### Kullanılabilir MCP Araçları:
* `vector_drive(distance_mm, speed_mmps)`: Robotu milimetre cinsinden sürer.
* `vector_turn(angle_deg, speed_dps)`: Robotu kendi ekseninde döndürür.
* `vector_set_head_angle(angle_deg)`: Kafa açısını ayarlar (-22° ile +45°).
* `vector_set_lift_height(height)`: Kaldırma kolunu ayarlar (0.0 - 1.0).
* `vector_say_text(text)`: Vector'ün hoparlöründen Türkçe ses çalar.
* `vector_show_screen(expression)`: 184x96 OLED ekranda ifade gösterir.
* `camera_move_ptz(pan_arcsec, tilt_arcsec)`: Insta360 Link 2'yi arcsecond cinsinden yönlendirir.
* `camera_set_desk_view()`: Kamerayı masaya 90 derece eğer (-288000 arcsec).
* `system_wake_pc()`: PC kapalıysa Wake-on-LAN sihirli paketini fırlatır.

---

## ⚡ Arduino UNO Q Çift Beyin (STM32U585) Kurulumu

1. Arduino IDE 2.x'te **Arduino UNO Q** kart profilini seçin.
2. `mcu_sketch/uno_q_status_matrix.ino` dosyasını açın.
3. Kodu kartın STM32U585 mikrodenetleyicisine yükleyin.
4. Kartın üzerindeki **8×13 mavi LED matrisi**; PC açık/kapalı, dinleme, konuşma ve Vector durum ikonlarını anlık olarak gösterecektir.

---

## 📄 Lisans

Bu proje MIT lisansı altında açık kaynak olarak geliştirilmektedir.
Anki ve Vector, Digital Dream Labs (DDL)'in tescilli ticari markalarıdır.

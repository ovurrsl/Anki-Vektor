# Anki Vector 2.0 + Arduino UNO Q + RTX 5070 — Tam Oturum Hafızası ve Devir Teslim Belgesi (Session Handoff)

> **Amaç:** Bu dosya, bulut oturumunda yapılan tüm araştırmaların, alınan mimari kararların, donanım analizlerinin, yazılan kodların ve çözülen sorunların **hiçbir bilgisinin kaybolmaması** ve **Local Mode (Yerel Antigravity / OpenCode / Claude Code / Gemini)** ortamına geçildiğinde yapay zeka ajanının kaldığı yerden %100 hakimiyetle devam etmesi için oluşturulmuştur.

---

## 1. Kullanıcının Donanım ve Yazılım Envanteri (Mülakat / Grill-Me Sonuçları)

1. **Şu An Fiziksel Olarak Elde Olan ve Bilgisayara Bağlı Donanımlar:**
   - **Arduino UNO Q 4GB (`ABX00173`)**:
     - **MPU (Beyin 1)**: Qualcomm Dragonwing QRB2210 (4 çekirdek Cortex-A53 @ 2.0 GHz, Adreno 702 GPU, 4 GB LPDDR4X RAM, 32 GB eMMC, Debian Linux OS).
     - **MCU (Beyin 2)**: STMicroelectronics STM32U585 (Cortex-M33 @ 160 MHz, Zephyr RTOS, üzerinde **8×13 Mavi Monokrom LED Matris**).
     - **Durum**: Kullanıcının Windows 11 bilgisayarına USB üzerinden bağlı.
   - **Masaüstü İş İstasyonu (PC Workstation)**:
     - **İşletim Sistemi**: Windows 11 (`C:\Users\ovurr\Desktop\Anki-Vektor`).
     - **GPU**: NVIDIA GeForce RTX 5070 (12 GB GDDR7 VRAM) — yerel Qwen 2.5 / Qwen 3-VL ve CosyVoice2 / Piper TTS için.
     - **NPU**: Intel Core Ultra 200S (Arrow Lake) entegre **NPU 3 (~36 TOPS)** — OpenVINO (`device="NPU"`) ile GPU VRAM'ini hiç harcamadan 7/24 kamera/ses işleme için.
   - **Bulut & Kodlama Ajanları**:
     - **Google AI Pro (Gemini Pro / Live API)** aboneliği mevcut.
     - **OpenCode** ve **Claude Code** yerel bilgisayarda kullanılıyor (`.mcp.json` ve `opencode.json` kök dizine eklendi).

2. **Henüz Fiziksel Olarak Alınmamış (Simülasyon / Mock Modunda Çalışan) Donanımlar:**
   - **Anki Vector 2.0 Robot** (`MOCK_ROBOT=True` varsayılan olarak aktif; fiziksel robot geldiğinde `.env` içinden `MOCK_ROBOT=False` yapılacak).
   - **Insta360 Link 2 PTZ 4K Kamera** (`MOCK_CAMERA=True` varsayılan olarak aktif; dinamik Pillow JPEG masa simülatörü çalışıyor).

---

## 2. Üç Katmanlı (Three-Tier) Bedenlenmiş Yapay Zeka Mimarisi

```
+-----------------------------------------------------------------------------------+
| KATMAN 1: 7/24 NÖBETÇİ GATEWAY (Arduino UNO Q 4GB - ~2.5W Güç Tüketimi)           |
|  - QRB2210 Linux MPU: gateway/main.py (Port 8000), Wake-on-LAN (UDP Port 9)       |
|  - STM32U585 MCU: mcu_sketch/uno_q_status_matrix.ino (8x13 Mavi LED Matris)       |
|  - Half-Duplex AEC: gateway/audio_pipeline.py (400ms kuyruk + 24kHz->16kHz soxr)  |
|  - Epizodik Hafıza: memory/db.py (sqlite-vec vec0 768-boyutlu vektör tablosu)     |
+-----------------------------------------+-----------------------------------------+
                                          |
                 LAN / Wi-Fi / USB Serial | (ArduinoBridge RPC & pyserial COM*)
                                          v
+-----------------------------------------------------------------------------------+
| KATMAN 2: AĞIR İŞ İSTASYONU (Windows 11 PC - RTX 5070 12GB + Intel NPU 3)         |
|  - pc_agent/server.py (Port 8080) & Web Dashboard (http://localhost:8080/dashboard)|
|  - pc_agent/camera_ptz.py: Insta360 Link 2 (1° = 3600 arcsec, step=3600)          |
|  - pc_agent/npu_engine.py: Intel NPU 3 OpenVINO yüz/nesne algılama                |
|  - pc_agent/llm_router.py: Gemini Live API + RTX 5070 Ollama + Claude Code Router |
+-----------------------------------------+-----------------------------------------+
                                          |
                           Model Context Protocol (FastMCP)
                                          v
+-----------------------------------------------------------------------------------+
| KATMAN 3: AJAN BEYNİ VE EKOSİSTEM (brain_mcp/server.py - 18 MCP Aracı)            |
|  - Vector 2.0 Hareket, Kafa/Kol, Göz İfadesi, Türkçe Konuşma, Şarj İstasyonu      |
|  - Arduino UNO Q 8x13 LED Matris Kontrolü & Otomatik Flash (.ino)                 |
|  - ovurrsl/arduino-room-thermostat (BLE GIGA R1 + UNO R4 Oda Termostatı Köprüsü)  |
|  - ovurrsl/Dynamic-Lighting (AmbiFlux 108-LED WS2812B 'Awa' Protokolü Köprüsü)    |
|  - Google Calendar (gcalendar) & GitHub (gh) DevOps Asistanı Araçları             |
+-----------------------------------------------------------------------------------+
```

---

## 3. Depodaki Tüm Modüller ve Dosya Haritası

| Dosya Yolu | Görevi ve İçeriği |
| :--- | :--- |
| `CALISTIR_LOCAL.bat` | **Windows 11 Tek Tıkla Başlatıcı:** `git pull` yapar, `scripts/auto_setup_windows_and_uno_q.ps1` scriptini çağırarak taşınabilir `uv.exe` + `Python 3.11` + `arduino-cli.exe` kurar, USB'deki Arduino UNO Q'yu flaşlar ve `http://localhost:8080/dashboard` sayfasını açar. |
| `scripts/auto_setup_windows_and_uno_q.ps1` | Windows PC üzerinde Python `PATH`'te olmasa bile `.tools/uv.exe` indirip `.venv` içinde Python 3.11 oluşturan, `COM*` portlarını tarayan, STM32U585'e `.ino` yükleyen ve Port 8000/8080 sunucularını başlatan PowerShell scripti. |
| `mcu_sketch/uno_q_status_matrix.ino` | Arduino UNO Q üzerindeki STM32U585 mikrodenetleyicisi için yazılmış C++ kodu. Hem Linux `ArduinoBridge` RPC (`Bridge.bind("set_status", onSetStatus)`) hem de doğrudan **USB Serial (`115200 baud`, `SET_STATUS:2` vb.)** komutlarını dinleyerek 8×13 Mavi LED Matrisi (`1=STANDBY`, `2=PC_ON`, `3=LISTENING`, `4=SPEAKING`, `5=VECTOR_OK`, `9=ERROR`) günceller. |
| `gateway/uno_q_bridge.py` | Python `pyserial` kullanarak Windows `COM*` ve Linux `/dev/tty*` portlarını otomatik keşfeden, `SET_STATUS:N` gönderen ve `arduino-cli` ile tek tıkla `.ino` derleyip yükleyen köprü sınıfı (`UnoQBridge`). |
| `gateway/ecosystem_bridge.py` | Kullanıcının diğer GitHub repolarıyla tam entegrasyon modülü:<br>1) `RoomThermostatBridge`: `ovurrsl/arduino-room-thermostat` (`BLE UUID 6E400001-B5A3-F393-E0A9-E50E24DCCA9E`, IEEE-754 Float32 sıcaklık ve histerezis röle kontrolü).<br>2) `AmbiFluxBridge`: `ovurrsl/Dynamic-Lighting` (`Awa` seri protokolü + 3-byte Fletcher Checksum ile 108-LED WS2812B monitör arkası aydınlatmayı Vector'ün duygularıyla senkronize eder). |
| `gateway/vector_bridge.py` | `wirepod-vector-sdk` sarmalayıcısı ve fiziksel robot yokken tüm kinematik/batarya/şarj/ekran durumlarını simüle eden `MockVectorRobot` sınıfı. |
| `gateway/audio_pipeline.py` | **Half-Duplex AEC (400ms eko sönümleme kuyruğu)** + `soxr` ile Gemini 24kHz PCM sesini Vector'ün istediği 16kHz 16-bit mono WAV formatına dönüştüren boru hattı. |
| `gateway/wol_sentinel.py` | Arduino UNO Q üzerinden masaüstü PC'nin MAC adresine UDP Port 9 Magic Packet fırlatan ve TCP soketiyle PC'nin açık/kapalı olduğunu izleyen nöbetçi. |
| `memory/db.py` & `memory/schema.sql` | `sqlite-vec` (`vec0` sanal tablosu) ve NumPy kosinüs benzerliği yedekli uzun süreli epizodik hafıza yöneticisi (`MemoryManager`). |
| `pc_agent/camera_ptz.py` | Insta360 Link 2 (`USB ID 2e1a:4c04`) için `3600 arcsec` (`1°`) kuantizasyonlu Pan/Tilt kontrolcüsü, `jweaver60/link-studio` UVC donanım modları (`normal`, `deskview`, `ai_tracking`, `whiteboard`, `overhead`, `privacy`) ve Pillow tabanlı canlı `MockCamera`. |
| `pc_agent/server.py` & `pc_agent/templates/dashboard.html` | Port 8080 üzerinde çalışan FastAPI sunucusu ve Web Dashboard. İçinde Vector yön/kafa/kol kontrolü, Insta360 kamera simülasyonu, **Arduino UNO Q 8×13 LED Matris canlı seçici + COM Port Tarayıcı + Tek Tıkla `.ino` Yükleyici**, BLE Termostat ve AI Sohbet bulunur. |
| `brain_mcp/server.py` & `brain_mcp/tools.py` | Claude Code, OpenCode ve Gemini için **18 adet MCP aracı** sunan FastMCP sunucusu. |
| `.mcp.json` & `opencode.json` | Klasör yerel bilgisayarda açıldığında MCP sunucusunu otomatik bağlayan yapılandırma dosyaları. |
| `.agents/skills/anki-vector-uno-q-architect/SKILL.md` | Yerel ajanların bu mimariyi otomatik tanıması için kaydedilmiş özel Skill dosyası. |

---

## 4. Çözülen Kritik Sorunlar ve Local Mode'da Yapılacak İlk İşlem

1. **Sorun 1 — Bulut VM İzolasyonu:**
   - Bulut oturumundaki terminal komutları Google Cloud Linux VM üzerinde çalıştığı için kullanıcının Windows bilgisayarındaki fiziksel USB portlarını göremiyordu.
   - **Çözüm:** Tüm yerel donanım tarama (`pyserial`), `arduino-cli` indirme ve sunucu başlatma işlemleri `CALISTIR_LOCAL.bat` ve `scripts/auto_setup_windows_and_uno_q.ps1` içine alındı.
2. **Sorun 2 — Windows PC'de `'python' is not recognized` ve PowerShell Parametre Hatası:**
   - Kullanıcının Windows `PATH` ortam değişkeninde `python` ve `pip` tanımlı değildi; bu yüzden `.venv` oluşmamış ve `localhost:8080` başlamamıştı.
   - **Çözüm (`commit 0798330`):** `scripts/auto_setup_windows_and_uno_q.ps1` güncellendi. Artık sistemde Python kurulu olmasa bile script otomatik olarak `.tools/uv.exe` indiriyor, `.venv` içine **taşınabilir Python 3.11** kuruyor, tüm paketleri yüklüyor, `localhost:8080`'in açıldığını test ediyor ve tarayıcıyı açıyor.

### Local Mode'a Geçtiğinizde Ajanın veya Sizin Yapacağınız İlk Komut:
Yerel bilgisayarınızda (`C:\Users\ovurr\Desktop\Anki-Vektor` dizininde) terminali açıp:
```powershell
git pull origin main
.\CALISTIR_LOCAL.bat
```
komutunu çalıştırmak veya yerel Antigravity / OpenCode / Claude Code ajanına **"SESSION_HANDOFF.md dosyasını oku ve localde başlat"** demektir.

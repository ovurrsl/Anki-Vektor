# Implementation Plan: Üç Katmanlı Bedenlenmiş Yapay Zeka (Embodied AI) Hibrit Mimarisi

Bu uygulama planı; **Anki Vector 2.0** (fiziksel beden), **Arduino UNO Q 4GB** (7/24 açık nöbetçi uç ağ geçidi), **Masaüstü PC (NVIDIA GeForce RTX 5070 + Intel Core Ultra NPU)** ve **Google Gemini Pro Live API** katmanlarını birleştiren hibrit yapay zeka mimarisinin [`ovurrsl/Anki-Vektor`](https://github.com/ovurrsl/Anki-Vektor) deposunda uçtan uca inşa edilmesini kapsar.

Kullanıcının elinde şu anda **Arduino UNO Q**, **RTX 5070 + NPU Masaüstü PC** ve **Google Pro hesabı** bulunmakta; **Vector 2.0** ve **Insta360 Link 2** henüz fiziksel olarak bulunmamaktadır. Bu nedenle mimari, **birebir donanım simülasyonu ve sahte (mock) ajan katmanı** ile tasarlanacak; mevcut donanımlarla anında çalıştırılıp test edilebilecek ve fiziksel donanımlar eklendiğinde tek bir konfigürasyon bayrağıyla (`MOCK_MODE=false`) canlı çalışmaya geçecektir.

---

## User Review Required

> [!IMPORTANT]
> **Donanım Simülasyonu (Mock Katmanı) Varsayılan Olarak Aktiftir:**
> Robot ve kamera henüz fiziksel olarak elinizde olmadığı için `MOCK_ROBOT=True` ve `MOCK_CAMERA=True` bayrakları varsayılan gelecektir. Sistem, Vector'ün göz ekranını, bataryasını, kafa/kol motorlarını ve Insta360 Link 2'nin motor açılarını ve video akışını sanal olarak simüle edecek ve PC'deki Web Gösterge Paneli (Dashboard) üzerinden canlı görselleştirecektir.

> [!NOTE]
> **Modern Python & Wire-Pod Uyumu:**
> Orijinal ve terk edilmiş `anki-vector` yerine güncel ve Python 3.11/3.12 uyumlu **`wirepod-vector-sdk`** referans alınmıştır. Kodlar doğrudan `anki_vector` standart SDK API'leriyle yazılacak, böylece ileride Wire-Pod ile eşleştiğinde kod değişikliği gerekmeyecektir.

> [!TIP]
> **Arduino UNO Q Çift Beyin (Dual-Brain) Desteği:**
> Qualcomm QRB2210 (Debian MPU) üzerinde Python Asyncio Gateway çalışırken; STM32U585 (Zephyr MCU) için kartın üzerindeki 8×13 mavi LED matrisi robot ve PC durum göstergesine dönüştüren resmi `ArduinoBridge` uyumlu bir C++ sketch'i (`uno_q_status_matrix.ino`) sağlanacaktır.

---

## Open Questions

Tüm mimari sorular `/grill-me` mülakatında yanıtlanmış ve tasarım kararları netleştirilmiştir. Açık soru bulunmamaktadır.

---

## Proposed Changes

Proje, [`/home/antigravity/ovurrsl/Anki-Vektor`](file:///home/antigravity/ovurrsl/Anki-Vektor) kök dizininde modüler bir monorepo olarak yapılandırılacaktır:

```text
ovurrsl/Anki-Vektor/
├── gateway/                 # Arduino UNO Q 7/24 Nöbetçi Ağ Geçidi
│   ├── __init__.py
│   ├── config.py            # Konfigürasyon ve ortam değişkenleri
│   ├── main.py              # Asyncio ana olay döngüsü ve orkestratör
│   ├── vector_bridge.py     # Gerçek wirepod-vector-sdk ve MockVectorRobot köprüsü
│   ├── audio_pipeline.py    # Half-Duplex AEC, 24k->16k ses dönüşümü ve VAD
│   ├── wol_sentinel.py      # Wake-on-LAN sihirli paket fırlatıcı ve PC ping nöbetçisi
│   ├── intent_parser.py     # PC ve internet kapalıyken yerel niyet çözümleyici
│   └── requirements.txt     # UNO Q hafif Python bağımlılıkları
├── pc_agent/                # RTX 5070 + Intel NPU Masaüstü PC İş İstasyonu Ajanı
│   ├── __init__.py
│   ├── config.py            # PC Ajanı konfigürasyonu
│   ├── server.py            # FastAPI + FastMCP HTTP/SSE sunucusu + Web Dashboard
│   ├── camera_ptz.py        # Insta360 Link 2 arcsecond PTZ sürücüsü + MockCamera
│   ├── npu_engine.py        # Intel NPU OpenVINO Whisper-Turbo & YOLOv8n yöneticisi
│   ├── llm_router.py        # Gemini Live API, Yerel Qwen LLM ve Claude Code yönlendiricisi
│   ├── static/              # Dashboard web arayüzü dosyaları (CSS/JS)
│   ├── templates/
│   │   └── dashboard.html   # Canlı gösterge paneli (Robot, Kamera, VRAM, NPU izleme)
│   └── requirements.txt     # PC iş istasyonu bağımlılıkları
├── brain_mcp/               # Model Context Protocol (FastMCP) Standart Araç Seti
│   ├── __init__.py
│   ├── server.py            # FastMCP araç tanımları (VectorClaw mantığı)
│   └── tools.py             # drive, head, lift, say, screen, camera_ptz, wake_pc araçları
├── memory/                  # sqlite-vec Kalıcı Epizodik Hafıza Katmanı
│   ├── __init__.py
│   ├── db.py                # sqlite-vec / vec0 sanal tablo motoru ve benzerlik araması
│   └── schema.sql           # Vektör ve ilişkisel hafıza tabloları
├── mcu_sketch/              # Arduino UNO Q STM32U585 Gerçek Zamanlı MCU Kodu
│   └── uno_q_status_matrix.ino # 8x13 Mavi LED matrisi durum ekranı ve Bridge RPC
├── tests/                   # Otomatik Test Paketi (Pytest)
│   ├── __init__.py
│   ├── test_gateway.py      # WoL, ses resampler ve intent parser testleri
│   ├── test_vector_mock.py  # Mock Vector robot durumları ve komut testleri
│   ├── test_camera_ptz.py   # Arcseconds PTZ ve Mock kamera testleri
│   ├── test_memory.py       # sqlite-vec yerel hafıza yazma/okuma testleri
│   └── test_mcp_tools.py    # FastMCP araç çağrı testleri
├── scripts/                 # Kurulum ve Çalıştırma Betikleri
│   ├── setup_uno_q.sh       # Headless Debian ve bağımlılık kurulum betiği
│   ├── run_gateway.sh       # Gateway başlatıcı
│   ├── run_pc_agent.bat     # Windows 11 PC Ajanı başlatıcı
│   └── run_pc_agent.sh      # Linux PC Ajanı başlatıcı
├── systemd/                 # Linux Arka Plan Servis Tanımları
│   └── vector-gateway.service # UNO Q 7/24 systemd unit dosyası
├── .env.example             # Ortam değişkenleri şablonu
├── .gitignore               # Python, cache ve sanal ortam filtreleri
└── README.md                # Kapsamlı kurulum, mimari ve çalıştırma kılavuzu
```

---

### [Component 1] Arduino UNO Q Gateway Katmanı (`gateway/`)

#### [NEW] `gateway/config.py`
Sistem ortam değişkenlerini (`.env`) yükleyen, `MOCK_ROBOT`, `MOCK_CAMERA`, PC IP/MAC adresleri, portlar ve zaman aşımlarını yöneten modül.

#### [NEW] `gateway/vector_bridge.py`
Hem gerçek robotu (`wirepod-vector-sdk`) hem de fiziksel donanım yokken çalışan `MockVectorRobot` sınıfını içeren sarmalayıcı. Robotun x,y konumu, baş açısı, kaldırma kolu yüksekliği, pil seviyesi, dock durumu ve OLED ekran piksellerini bellek içi bir modelde tutar.

#### [NEW] `gateway/wol_sentinel.py`
* UDP Port 9 üzerinden standart 102 baytlık Wake-on-LAN Magic Packet (`FF*6 + MAC*16`) gönderir.
* Arka planda periyodik olarak PC'nin IP adresini ICMP ping veya TCP port kontrolüyle dinler; PC açık/kapalı durumunu atomik olarak günceller.

#### [NEW] `gateway/audio_pipeline.py`
* **Half-Duplex AEC Mantığı:** Vector konuşurken (`is_speaking=True`) mikrofon girdisini yazılımsal olarak susturur; konuşma bitince 400 ms oda sönümleme gecikmesi ekleyip dinlemeyi tekrar açar.
* **Ses Dönüşümü (Resampling):** Gemini Live API veya PC'den gelen 24,000 Hz 16-bit PCM akışını Vector'ün kabul ettiği 16,000 Hz Mono WAV formatına gerçek zamanlı dönüştürür.

#### [NEW] `gateway/intent_parser.py`
PC ve internet kapalıyken UNO Q üzerinde çevrimdışı çalışan regex ve anlamsal kural tabanlı niyet ayrıştırıcı ("saat kaç", "alarm kur", "pc aç", "batarya durumu", "şarj yuvasına dön").

#### [NEW] `gateway/main.py`
Tüm ağ geçidi servislerini (`vector_bridge`, `wol_sentinel`, `audio_pipeline`, `memory`) `asyncio` döngüsünde başlatan ve yöneten ana giriş noktası.

---

### [Component 2] Masaüstü PC Ajanı & Gösterge Paneli (`pc_agent/`)

#### [NEW] `pc_agent/server.py`
* FastAPI tabanlı web sunucusu:
  * `/api/v1/status`: PC, GPU, NPU, Gateway ve Vector telemetrisi.
  * `/api/v1/camera/snapshot`: Insta360 veya Mock kameradan anlık JPEG kare döndürür.
  * `/api/v1/camera/ptz`: Kameranın pan/tilt/zoom değerlerini günceller.
  * `/api/v1/robot/command`: Robota doğrudan hareket veya ses emri verir.
  * `/dashboard`: Web arayüzünü sunar.
  * `/sse`: FastMCP SSE bağlantı uç noktası.

#### [NEW] `pc_agent/camera_ptz.py`
* Insta360 Link 2 için **arcseconds** (1° = 3600 yay-saniyesi, step=3600) hesaplamasıyla `v4l2-ctl` komutları üretir.
* `MOCK_CAMERA=True` olduğunda sanal bir masaüstü test karesi (Vector'ün masadaki koordinatını gösteren dinamik bir simülasyon karesi) üretir.

#### [NEW] `pc_agent/npu_engine.py`
* Intel Core Ultra NPU 3 (Arrow Lake-S) üzerinde OpenVINO çalışma zamanını yönetir.
* Donanımda NPU algılanamazsa (veya sürücü henüz kurulmadıysa) CPU fallback modunda çalışarak sistemin çökmesini engeller.

#### [NEW] `pc_agent/llm_router.py`
* Google Gemini Pro Live API (`google-genai` WebSocket), RTX 5070 yerel `llama-server` (Qwen 2.5 7B/14B Q4_K_M) ve Claude Code CLI arasında akıllı yönlendirme yapar.

#### [NEW] `pc_agent/templates/dashboard.html`
* Modern, koyu temalı (dark-mode), Tailwind/vanilla CSS ile tasarlanmış canlı Web Dashboard:
  * **Sanal Vector Durumu:** Kafa açısı, kol konumu, göz ifadesi, batarya ve şarj yuvası göstergesi.
  * **Insta360 Kamera Önizlemesi:** Canlı kare, Pan/Tilt kaydırıcıları ve DeskView butonu.
  * **Donanım Telemetrisi:** PC uyanıklık durumu, RTX 5070 VRAM kullanımı, NPU aktifliği ve UNO Q ping durumu.
  * **Canlı Log Konsolu:** Olayları ve ses etkileşimlerini gerçek zamanlı gösteren terminal ekranı.

---

### [Component 3] Model Context Protocol (MCP) Omurgası (`brain_mcp/`)

#### [NEW] `brain_mcp/server.py` & `brain_mcp/tools.py`
FastMCP kütüphanesi ile dış yapay zeka ajanlarına açılan standart araçlar:
* `vector_drive(distance_mm, speed_mmps)`: Robotu ileri/geri sürer.
* `vector_turn(angle_deg, speed_dps)`: Robotu kendi ekseninde döndürür.
* `vector_set_head_angle(angle_deg)`: Robotun kafa açısını (-22° ile +45°) ayarlar.
* `vector_set_lift_height(height_0_to_1)`: Kaldırma kolunu ayarlar.
* `vector_say_text(text, language)`: Vector hoparlöründen Türkçe ses çalar.
* `vector_show_screen(face_expression)`: Göz ekranında ifade gösterir.
* `camera_move_ptz(pan_arcsec, tilt_arcsec)`: Insta360 Link 2 motorlarını sürer.
* `camera_get_snapshot()`: Masanın anlık kuşbakışı karesini döndürür.
* `system_wake_pc()`: PC kapalıysa Wake-on-LAN sihirli paketini tetikler.
* `memory_query(query, limit)`: Epizodik hafızadan geçmiş anıları çeker.
* `memory_store(fact, category)`: Kullanıcı hakkındaki yeni bilgiyi hafızaya yazar.

---

### [Component 4] Kalıcı Hafıza Katmanı (`memory/`)

#### [NEW] `memory/schema.sql` & `memory/db.py`
* `sqlite-vec` yüklü olduğunda doğrudan `vec0` sanal tablosunu ve ilişkisel `memory_meta` tablosunu kullanır.
* `sqlite-vec` kütüphanesinin derlenmediği ortamlarda sistemin çökmemesi için saf Python/NumPy kosinüs benzerliği (cosine similarity) yedeğine (fallback) sahip hibrit motor içerir.

---

### [Component 5] STM32U585 MCU Kodu (`mcu_sketch/`)

#### [NEW] `mcu_sketch/uno_q_status_matrix.ino`
* Arduino UNO Q'nun STM32U585 mikrodenetleyicisi için C++ kodu:
  * 8×13 mavi LED matrisi üzerinde özel piksel simgeleri:
    * `ICON_BOOT`: Açılış animasyonu (ilk 30 sn).
    * `ICON_PC_ON`: PC uyanık / bağlı simgesi.
    * `ICON_PC_OFF`: PC kapalı / nöbetçi simgesi.
    * `ICON_LISTEN`: Ses dinleniyor simgesi.
    * `ICON_SPEAK`: Robot konuşuyor simgesi.
    * `ICON_VECTOR_OK`: Vector gRPC bağlantısı aktif.
    * `ICON_ERR`: Ağ veya servis hatası.
  * Linux MPU'dan `ArduinoBridge` RPC üzerinden `set_status(status_code)` çağrılarını dinler ve anında matrisi günceller.

---

### [Component 6] Testler, Betikler ve Dokümantasyon (`tests/`, `scripts/`, `README.md`)

#### [NEW] `tests/test_*.py`
* Tüm modüller için otomatik `pytest` test paketi:
  * Mock Vector motor ve sensör doğrulaması
  * WoL paket formatı doğrulaması
  * 24k -> 16k ses örnekleme doğrulaması
  * Half-duplex ses susturucu durum makinesi testi
  * sqlite-vec / cosine similarity hafıza testi
  * FastMCP araç yürütme ve şema doğrulaması
  * FastAPI REST uç noktaları testi

#### [NEW] `README.md`
* Sistemin kurulumu, ortam değişkenlerinin ayarlanması, Arduino UNO Q üzerinde headless çalıştırma, PC Ajanının başlatılması ve fiziksel robot/kamera entegrasyonuna geçiş adımlarını detaylandıran kapsamlı kılavuz.

---

## Verification Plan

### Automated Tests
1. **Birim ve Entegrasyon Testleri:**
   ```bash
   cd /home/antigravity/ovurrsl/Anki-Vektor
   pytest -v tests/
   ```
2. **FastAPI ve MCP Uç Nokta Doğrulaması:**
   FastAPI TestClient ile `/api/v1/status`, `/api/v1/camera/snapshot`, `/api/v1/robot/command` ve FastMCP araç fonksiyonlarının çağrılması.
3. **Ses Dönüşüm Doğrulaması:**
   24,000 Hz sentetik ses dalgasının 16,000 Hz mono PCM formatına veri kaybı ve hata olmadan dönüştürüldüğünün matematiksel doğrulaması.
4. **Hafıza Vektör Arama Testi:**
   `memory/db.py` üzerinden 768 boyutlu test embedding'leri ile kayıt yapılması ve en yakın benzerlik sorgusunun doğrulanması.

### Manual Verification
1. **Web Dashboard Doğrulaması:**
   `pc_agent/server.py` çalıştırılarak tarayıcıdan sanal Vector arayüzünün, sanal kamera kontrollerinin ve telemetri kartlarının görsel olarak kontrol edilmesi.
2. **Git ve GitHub Senkronizasyonu:**
   Oluşturulan tüm kod tabanının `git status`, `git log` ve `git push` ile `ovurrsl/Anki-Vektor` reposunun `main` dalına eksiksiz aktarıldığının doğrulanması.

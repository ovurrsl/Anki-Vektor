# Anki Vector 2.0 + Arduino UNO Q + RTX 5070 Hibrit Yapay Zeka Mimarisi — Tam Kurulum ve Entegrasyon Raporu

Tüm **Skills**, **Plugins** (`github`, `gcalendar`, `gdrive`, `gdocs`, `gsheets`, `gslides`), **MCP Sunucuları** (`Anki-Vector-Brain`) ve **Arduino UNO Q (`ABX00173`) Dual-Brain Köprüsü** taranmış, projeye entegre edilmiş, test edilmiş ve [`ovurrsl/Anki-Vektor`](https://github.com/ovurrsl/Anki-Vektor) GitHub deponuza gönderilmiştir.

---

## 1. Yüklenen ve Entegre Edilen Skill, Plugin ve MCP Bileşenleri

| Katman | Bileşen / Dosya | Açıklama |
| :--- | :--- | :--- |
| **Özel Mimari Skill** | [SKILL.md](file:///home/antigravity/ovurrsl/Anki-Vektor/.agents/skills/anki-vector-uno-q-architect/SKILL.md) | `anki-vector-uno-q-architect` adıyla hem global ortama hem de repo içine kaydedildi. Tüm ajanlar artık Vector + UNO Q + RTX 5070 mimarisini otomatik tanır. |
| **Claude Code MCP** | [.mcp.json](file:///home/antigravity/ovurrsl/Anki-Vektor/.mcp.json) | Claude Code açıldığında `anki-vector-brain` MCP sunucusunu otomatik başlatır. |
| **OpenCode + Gemini MCP** | [opencode.json](file:///home/antigravity/ovurrsl/Anki-Vektor/opencode.json) | OpenCode üzerinde Gemini Pro / Qwen modellerinin tüm 15 fiziksel ve Workspace aracını kullanmasını sağlar. |
| **Arduino UNO Q Köprüsü** | [uno_q_bridge.py](file:///home/antigravity/ovurrsl/Anki-Vektor/gateway/uno_q_bridge.py) | Qualcomm Dragonwing QRB2210 (Linux) ile STM32U585 (8×13 Mavi LED Matris) arasında `ArduinoBridge` RPC / Serial / Simülasyon iletişimini yönetir. |
| **Genişletilmiş MCP Araçları** | [tools.py](file:///home/antigravity/ovurrsl/Anki-Vektor/brain_mcp/tools.py) & [server.py](file:///home/antigravity/ovurrsl/Anki-Vektor/brain_mcp/server.py) | Vector hareket/ses kontrolü, Insta360 Link 2 PTZ (`arcseconds`), Wake-on-LAN, UNO Q LED matrisi (`uno_q_set_led_matrix`), Google Takvim (`calendar_get_today_schedule`) ve GitHub (`github_get_repo_status`) araçlarını içerir. |
| **Tek Tıkla Windows + UNO Q Kurucu** | [auto_setup_windows_and_uno_q.ps1](file:///home/antigravity/ovurrsl/Anki-Vektor/scripts/auto_setup_windows_and_uno_q.ps1) | Windows PC'nizde USB'ye bağlı Arduino UNO Q kartını (`COM*` / `unoq.local`) otomatik bulur, STM32U585 LED kodunu flaşlar ve tüm servisleri başlatır. |

---

## 2. Kendi Bilgisayarınızda (Windows PC + Arduino UNO Q) Tek Komutla Çalıştırma

Bilgisayarınıza bağlı olan **Arduino UNO Q** kartınızı ve **RTX 5070 + NPU** sisteminizi devreye almak için Windows PowerShell'de şu 2 satırı çalıştırmanız yeterlidir:

```powershell
git clone https://github.com/ovurrsl/Anki-Vektor.git
cd Anki-Vektor
powershell -ExecutionPolicy Bypass -File .\scripts\auto_setup_windows_and_uno_q.ps1
```

> [!TIP]
> Bu script otomatik olarak:
> 1. USB üzerinden bağlı **Arduino UNO Q** (`COM` portu ve `unoq.local` RNDIS/SSH) bağlantısını tarar.
> 2. `arduino-cli` mevcutsa [uno_q_status_matrix.ino](file:///home/antigravity/ovurrsl/Anki-Vektor/mcu_sketch/uno_q_status_matrix.ino) kodunu STM32U585 mikrodenetleyicisine yükler.
> 3. `.venv` sanal ortamını ve `.env` ayarlarını oluşturur.
> 4. **Gateway (Port 8000)** ve **PC Workstation Agent (Port 8080)** servislerini başlatıp tarayıcınızda `http://localhost:8080/dashboard` adresini açar.

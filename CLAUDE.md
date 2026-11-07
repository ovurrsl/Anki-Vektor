# AGENTS.md & CLAUDE.md — Local Agent Context for `ovurrsl/Anki-Vektor`

When opening this repository in **Local Mode** (Antigravity Local, Claude Code, OpenCode, or Cursor), read these files immediately for full context:

1. **[SESSION_HANDOFF.md](SESSION_HANDOFF.md)** — Complete history of the cloud development session, user hardware inventory (Arduino UNO Q 4GB `ABX00173`, RTX 5070 12GB, Intel Core Ultra 200S NPU 3, Google AI Pro), solved issues, and next steps.
2. **[.agents/skills/anki-vector-uno-q-architect/SKILL.md](.agents/skills/anki-vector-uno-q-architect/SKILL.md)** — Hardware rules, arcsecond PTZ camera math, Half-Duplex AEC audio pipeline, `sqlite-vec` memory, and MCP tools.
3. **[docs/Vector_Hibrit_Yapay_Zeka_Mimarisi.md](docs/Vector_Hibrit_Yapay_Zeka_Mimarisi.md)** & **[docs/Anki_Vector_ve_Cozmo_Farkları.md](docs/Anki_Vector_ve_Cozmo_Farkları.md)** — Original Turkish architectural research documents.

## Quick Local Start (Windows 11)
Run in PowerShell or CMD inside the repository root:
```powershell
.\CALISTIR_LOCAL.bat
```
Or via PowerShell directly:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\auto_setup_windows_and_uno_q.ps1
```
This script automatically downloads portable `uv.exe` + Python 3.11 (even if Python is not in Windows `PATH`), installs dependencies into `.venv`, downloads `arduino-cli.exe`, detects the USB-connected Arduino UNO Q (`COM*`), flashes `mcu_sketch/uno_q_status_matrix.ino`, and launches:
- **UNO Q Gateway**: `http://localhost:8000`
- **PC Workstation Agent & Dashboard**: `http://localhost:8080/dashboard`

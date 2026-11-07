---
name: anki-vector-uno-q-architect
description: Build, configure, debug, and control the Three-Tier Embodied AI Hybrid Architecture for Anki Vector 2.0, Arduino UNO Q 4GB (ABX00173), RTX 5070 + Intel Core Ultra 200S NPU PC, and Google Gemini Pro Live API.
---

# Anki Vector 2.0 + Arduino UNO Q + RTX 5070 Hybrid AI Architect

## Architecture & Hardware Rules
- **Tier 1 (`gateway/`)**: Runs on **Arduino UNO Q 4GB (ABX00173)** (Qualcomm Dragonwing QRB2210 Linux MPU + STM32U585 Cortex-M33 MCU). Uses `gateway/uno_q_bridge.py` (`UnoQBridge`) to drive the 8×13 Blue LED Matrix (`IDLE`, `LISTENING`, `THINKING`, `WAKE_PC`, `ERROR`) and `gateway/wol_sentinel.py` to wake the PC via UDP Port 9 Magic Packet.
- **Tier 2 (`pc_agent/`)**: Runs on **RTX 5070 + Intel Core Ultra 200S NPU PC**. Controls **Insta360 Link 2** gimbal in **arcseconds** (`1° = 3600 arcsec`, `step = 3600`, Pan `[-480000, +480000]`, Tilt `[-300000, +320000]`, Desk View `-288000`). Runs OpenVINO NPU inference (`pc_agent/npu_engine.py`).
- **Tier 3 (`brain_mcp/` & `memory/`)**: Exposes 15 MCP tools via FastMCP (`brain_mcp/server.py`) for Vector control, PTZ camera, UNO Q LED matrix, Wake-on-LAN, Google Calendar (`calendar_get_today_schedule`), and GitHub (`github_get_repo_status`). Uses `sqlite-vec` (`vec0` virtual table) in `memory/db.py`.
- **Audio AEC (`gateway/audio_pipeline.py`)**: Enforces Half-Duplex Mute Window + 400ms Post-Playback Tail and `soxr` 24kHz-to-16kHz resampling.

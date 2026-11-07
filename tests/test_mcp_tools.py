"""
Unit tests for FastMCP Tools, Arduino UNO Q Dual-Brain Bridge, and Workspace Integrations.
"""

import json
from pathlib import Path
import pytest
from brain_mcp.tools import MCPToolRegistry
from gateway.uno_q_bridge import UnoQBridge
from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel


@pytest.mark.asyncio
async def test_mcp_tool_execution():
    bridge = VectorBridge(mock_mode=True)
    wol = WakeOnLanSentinel(pc_mac="00:11:22:33:44:55")
    uno_q = UnoQBridge()
    registry = MCPToolRegistry(bridge, wol, uno_q=uno_q)

    # Test vector_drive
    res_drive = await registry.vector_drive(50.0, 50.0)
    assert "drove 50.0mm" in res_drive

    # Test vector_turn
    res_turn = await registry.vector_turn(90.0)
    assert "turned 90.0 degrees" in res_turn

    # Test vector_set_head_angle
    res_head = await registry.vector_set_head_angle(25.0)
    assert "25.0°" in res_head

    # Test vector_say_text
    res_say = await registry.vector_say_text("Merhaba MCP")
    assert "Vector said" in res_say

    # Test vector_get_telemetry
    status = await registry.vector_get_telemetry()
    assert status["connected"] is True

    # Test camera_move_ptz
    res_cam = await registry.camera_move_ptz(7200, -7200)
    assert "Pan=7200" in res_cam

    # Test system_wake_pc
    res_wol = await registry.system_wake_pc()
    assert "Wake-on-LAN" in res_wol
    assert uno_q.current_state == "WAKE_PC"


@pytest.mark.asyncio
async def test_uno_q_bridge_and_workspace_mcp_tools():
    bridge = VectorBridge(mock_mode=True)
    wol = WakeOnLanSentinel(pc_mac="00:11:22:33:44:55")
    uno_q = UnoQBridge()
    registry = MCPToolRegistry(bridge, wol, uno_q=uno_q)

    # Test UNO Q 8x13 LED Matrix states
    led_res = await registry.uno_q_set_led_matrix("THINKING")
    assert led_res["state"] == "THINKING"
    assert len(led_res["matrix_bitmap"]) == 8
    assert len(led_res["matrix_bitmap"][0]) == 13

    hw_status = await registry.uno_q_get_hardware_status()
    assert "STM32U585" in hw_status["mcu"]
    assert hw_status["led_state"] == "THINKING"

    # Test Google Calendar tool fallback/integration
    cal_res = await registry.calendar_get_today_schedule(announce_via_vector=True)
    assert "summary_tr" in cal_res
    assert "event_count" in cal_res

    # Test GitHub repo status tool
    gh_res = await registry.github_get_repo_status()
    assert gh_res["repository"] == "ovurrsl/Anki-Vektor"
    assert isinstance(gh_res["recent_commits"], list)


def test_mcp_and_opencode_config_files_exist():
    repo_root = Path(__file__).resolve().parent.parent
    mcp_json = repo_root / ".mcp.json"
    opencode_json = repo_root / "opencode.json"
    skill_md = repo_root / ".agents" / "skills" / "anki-vector-uno-q-architect" / "SKILL.md"

    assert mcp_json.exists()
    assert opencode_json.exists()
    assert skill_md.exists()

    mcp_data = json.loads(mcp_json.read_text(encoding="utf-8"))
    assert "anki-vector-brain" in mcp_data["mcpServers"]

    opencode_data = json.loads(opencode_json.read_text(encoding="utf-8"))
    assert "anki-vector-brain" in opencode_data["mcp"]

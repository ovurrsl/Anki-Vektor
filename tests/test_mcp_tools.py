"""
Unit tests for FastMCP Tools.
"""

import pytest
from brain_mcp.tools import MCPToolRegistry
from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel


@pytest.mark.asyncio
async def test_mcp_tool_execution():
    bridge = VectorBridge(mock_mode=True)
    wol = WakeOnLanSentinel(pc_mac="00:11:22:33:44:55")
    registry = MCPToolRegistry(bridge, wol)

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

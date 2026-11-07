"""
FastMCP Server for Vector Embodied AI.
Exposes MCP tools over stdio and SSE for Claude Code, OpenCode, Gemini Live, and Local Agents.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastmcp import FastMCP

from brain_mcp.tools import MCPToolRegistry
from gateway.config import config
from gateway.uno_q_bridge import UnoQBridge
from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel

logger = logging.getLogger("vector.mcp.server")

# Instantiate FastMCP server
mcp = FastMCP(
    "Anki-Vector-Brain",
    description="Model Context Protocol Server for Anki Vector 2.0, Arduino UNO Q, and Desk Embodied AI",
)

# Bridge and sentinel instances
bridge = VectorBridge(
    mock_mode=config.mock_robot,
    serial=config.vector_robot_serial,
    ip=config.vector_robot_ip,
)
wol = WakeOnLanSentinel(
    pc_mac=config.pc_mac_address,
    pc_ip=config.pc_host,
    pc_port=config.pc_port,
    wol_port=config.pc_wol_port,
)
uno_q = UnoQBridge()
registry = MCPToolRegistry(bridge, wol, uno_q=uno_q)


@mcp.tool()
async def vector_drive(distance_mm: float, speed_mmps: float = 50.0) -> str:
    """Drive Vector forward (positive mm) or backward (negative mm)."""
    return await registry.vector_drive(distance_mm, speed_mmps)


@mcp.tool()
async def vector_turn(angle_deg: float, speed_dps: float = 100.0) -> str:
    """Turn Vector in place (positive=counterclockwise, negative=clockwise)."""
    return await registry.vector_turn(angle_deg, speed_dps)


@mcp.tool()
async def vector_set_head_angle(angle_deg: float) -> str:
    """Set Vector head angle in degrees (-22.0 to 45.0)."""
    return await registry.vector_set_head_angle(angle_deg)


@mcp.tool()
async def vector_set_lift_height(height: float) -> str:
    """Set Vector lift arm height from 0.0 (ground) to 1.0 (top)."""
    return await registry.vector_set_lift_height(height)


@mcp.tool()
async def vector_say_text(text: str) -> str:
    """Speak text through Vector's internal speaker with Half-Duplex echo protection."""
    return await registry.vector_say_text(text)


@mcp.tool()
async def vector_show_screen(expression: str) -> str:
    """Set eye expression (neutral, happy, sarcastic, curious, surprised, sleepy, angry)."""
    return await registry.vector_show_screen(expression)


@mcp.tool()
async def vector_dock_charger() -> str:
    """Command Vector to navigate and dock onto its charger."""
    return await registry.vector_dock_charger()


@mcp.tool()
async def vector_get_telemetry() -> Dict[str, Any]:
    """Get current Vector robot telemetry (x, y, heading, battery, dock status)."""
    return await registry.vector_get_telemetry()


@mcp.tool()
async def system_wake_pc() -> str:
    """Send Wake-on-LAN Magic Packet to wake up the RTX 5070 / Intel NPU PC workstation."""
    return await registry.system_wake_pc()


@mcp.tool()
async def camera_move_ptz(pan_arcsec: int, tilt_arcsec: int) -> str:
    """
    Control Insta360 Link 2 PTZ gimbal.
    Angles are in arcseconds (1 deg = 3600 arcseconds, step=3600).
    Pan safe range: -480000 to +480000. Tilt safe range: -300000 to +320000.
    """
    return await registry.camera_move_ptz(pan_arcsec, tilt_arcsec)


@mcp.tool()
async def camera_set_desk_view() -> str:
    """Tilt the camera 80 degrees down to inspect electronics, papers, or the desk surface."""
    return await registry.camera_set_desk_view()


@mcp.tool()
async def uno_q_set_led_matrix(state: str) -> Dict[str, Any]:
    """
    Set the 8x13 Blue LED Matrix pattern on Arduino UNO Q (STM32U585) via Dual-Brain RPC.
    Valid states: IDLE, LISTENING, THINKING, WAKE_PC, ERROR.
    """
    return await registry.uno_q_set_led_matrix(state)


@mcp.tool()
async def uno_q_get_hardware_status() -> Dict[str, Any]:
    """Get Arduino UNO Q (QRB2210 + STM32U585) hardware status and 8x13 LED matrix bitmap."""
    return await registry.uno_q_get_hardware_status()


@mcp.tool()
async def calendar_get_today_schedule(announce_via_vector: bool = False) -> Dict[str, Any]:
    """Fetch today's Google Calendar events and optionally speak the summary through Vector."""
    return await registry.calendar_get_today_schedule(announce_via_vector=announce_via_vector)


@mcp.tool()
async def github_get_repo_status(repo: str = "ovurrsl/Anki-Vektor") -> Dict[str, Any]:
    """Get repository commit status for Desk DevOps monitoring."""
    return await registry.github_get_repo_status(repo=repo)


@mcp.tool()
async def thermostat_get_status(announce_via_vector: bool = False) -> Dict[str, Any]:
    """Read room temperature, humidity, IAQ, and relay state from ovurrsl/arduino-room-thermostat (BLE GIGA R1 + UNO R4)."""
    return await registry.thermostat_get_status(announce_via_vector=announce_via_vector)


@mcp.tool()
async def thermostat_set_temperature(setpoint_c: float, mode: str = "heating") -> Dict[str, Any]:
    """Set target room temperature (10-35°C) and mode (heating, cooling, fan, off) on the Arduino BLE Room Thermostat."""
    return await registry.thermostat_set_temperature(setpoint_c=setpoint_c, mode=mode)


@mcp.tool()
async def ambiflux_set_mood_light(mood: str) -> Dict[str, Any]:
    """Set the 108-LED WS2812B monitor ambilight (ovurrsl/Dynamic-Lighting Awa protocol) to match Vector's mood."""
    return await registry.ambiflux_set_mood_light(mood=mood)


def run_stdio():
    """Runs the FastMCP server over standard I/O (for Claude Code / OpenCode / Gemini CLI integration)."""
    mcp.run()


if __name__ == "__main__":
    run_stdio()

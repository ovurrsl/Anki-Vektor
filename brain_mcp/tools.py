"""
MCP Tools Definition for Anki Vector & Embodied AI Ecosystem.
Exposes standard tool interfaces to Claude Code, Gemini Live API, and Local LLMs.
Follows the VectorClaw MCP architecture pattern.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

import requests

from gateway.config import config
from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel

logger = logging.getLogger("vector.mcp.tools")


class MCPToolRegistry:
    """Registry of actionable tools callable by LLM agents via Model Context Protocol."""

    def __init__(self, bridge: VectorBridge, wol: WakeOnLanSentinel):
        self.bridge = bridge
        self.wol = wol

    async def vector_drive(self, distance_mm: float, speed_mmps: float = 50.0) -> str:
        """Drives the Vector robot straight forwards (positive) or backwards (negative)."""
        success = await self.bridge.drive_straight(distance_mm, speed_mmps)
        return (
            f"Robot drove {distance_mm:.1f}mm successfully."
            if success
            else "Failed to drive robot."
        )

    async def vector_turn(self, angle_deg: float, speed_dps: float = 100.0) -> str:
        """Turns the Vector robot in place (positive=counterclockwise, negative=clockwise)."""
        success = await self.bridge.turn_in_place(angle_deg, speed_dps)
        return (
            f"Robot turned {angle_deg:.1f} degrees successfully."
            if success
            else "Failed to turn robot."
        )

    async def vector_set_head_angle(self, angle_deg: float) -> str:
        """Sets Vector's head pitch angle in degrees (safe hardware range: -22.0 to 45.0)."""
        success = await self.bridge.set_head_angle(angle_deg)
        return (
            f"Head angle set to {angle_deg:.1f}°"
            if success
            else "Failed to set head angle."
        )

    async def vector_set_lift_height(self, height: float) -> str:
        """Sets Vector's front lift arm height (0.0=lowest on floor, 1.0=highest)."""
        success = await self.bridge.set_lift_height(height)
        return (
            f"Lift arm height set to {height:.2f}"
            if success
            else "Failed to set lift height."
        )

    async def vector_say_text(self, text: str) -> str:
        """Speaks Turkish or English text through Vector's internal speaker."""
        success = await self.bridge.say_text(text)
        return (
            f"Vector said: '{text}'"
            if success
            else "Failed to speak through Vector speaker."
        )

    async def vector_show_screen(self, expression: str) -> str:
        """Changes Vector's 184x96 eye display (options: neutral, happy, sarcastic, curious, surprised, sleepy, angry)."""
        success = await self.bridge.set_face_expression(expression)
        return (
            f"Display set to expression: '{expression}'"
            if success
            else "Failed to set face expression."
        )

    async def vector_dock_charger(self) -> str:
        """Commands Vector to return to its charging station dock."""
        success = await self.bridge.dock_on_charger()
        return (
            "Vector navigated and docked on charger."
            if success
            else "Failed to dock robot."
        )

    async def vector_get_telemetry(self) -> Dict[str, Any]:
        """Returns real-time status of Vector (coordinates, battery, head/lift, charger status)."""
        return self.bridge.get_status()

    async def system_wake_pc(self) -> str:
        """Sends Wake-on-LAN Magic Packet to power on the RTX 5070 / NPU desktop workstation."""
        success = self.wol.send_wol_packet()
        return (
            f"Wake-on-LAN packet transmitted to MAC {self.wol.pc_mac}."
            if success
            else "Failed to transmit WoL packet."
        )

    async def camera_move_ptz(self, pan_arcsec: int, tilt_arcsec: int) -> str:
        """
        Rotates the Insta360 Link 2 gimbal camera using arcseconds (1° = 3600 arcseconds).
        Step must be multiples of 3600.
        Safe ranges: Pan: -480000 to +480000; Tilt: -300000 to +320000.
        """
        try:
            url = f"http://{config.pc_host}:{config.pc_port}/api/v1/camera/ptz"
            resp = requests.post(
                url,
                json={"pan_arcsec": pan_arcsec, "tilt_arcsec": tilt_arcsec},
                timeout=2.0,
            )
            if resp.status_code == 200:
                return f"Camera gimbal moved to Pan={pan_arcsec}, Tilt={tilt_arcsec}"
        except Exception as e:
            logger.warning(f"Direct PC camera call failed ({e}), returning simulation response")
        return f"[MOCK/SIM] Camera moved to Pan={pan_arcsec} arcsec, Tilt={tilt_arcsec} arcsec."

    async def camera_set_desk_view(self) -> str:
        """Points the Insta360 Link 2 camera straight down at the desk surface (-80° = -288000 arcsec)."""
        return await self.camera_move_ptz(pan_arcsec=0, tilt_arcsec=-288000)

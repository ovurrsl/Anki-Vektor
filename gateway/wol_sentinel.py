"""
Wake-on-LAN and PC Health Sentinel Module.
Sends Magic Packets over UDP Port 9 to power on the RTX 5070 workstation.
Monitors PC online/offline status via periodic network probing.
"""

from __future__ import annotations

import asyncio
import binascii
import logging
import socket
from typing import Optional

logger = logging.getLogger("vector.wol")


def create_magic_packet(mac_address: str) -> bytes:
    """
    Constructs a standard 102-byte Wake-on-LAN Magic Packet.
    Format: 6 bytes of 0xFF followed by 16 repetitions of target 6-byte MAC address.
    """
    cleaned_mac = mac_address.replace(":", "").replace("-", "").replace(".", "").strip()
    if len(cleaned_mac) != 12:
        raise ValueError(f"Invalid MAC address format: '{mac_address}'. Must be 12 hex digits.")

    mac_bytes = binascii.unhexlify(cleaned_mac)
    return b"\xff" * 6 + mac_bytes * 16


class WakeOnLanSentinel:
    """
    Sentinel service running on Arduino UNO Q.
    Monitors PC status and wakes it up on demand.
    """

    def __init__(
        self,
        pc_mac: str = "AA:BB:CC:DD:EE:FF",
        pc_ip: str = "127.0.0.1",
        pc_port: int = 8080,
        wol_port: int = 9,
        broadcast_ip: str = "255.255.255.255",
    ):
        self.pc_mac = pc_mac
        self.pc_ip = pc_ip
        self.pc_port = pc_port
        self.wol_port = wol_port
        self.broadcast_ip = broadcast_ip
        self.is_pc_awake = False
        self._sentinel_task: Optional[asyncio.Task] = None

    def send_wol_packet(self, mac_override: Optional[str] = None) -> bool:
        """
        Sends the Wake-on-LAN magic packet over UDP broadcast.
        """
        target_mac = mac_override or self.pc_mac
        packet = create_magic_packet(target_mac)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(packet, (self.broadcast_ip, self.wol_port))
            logger.info(f"[WoL] Sent magic packet for MAC {target_mac} to {self.broadcast_ip}:{self.wol_port}")
            return True
        except Exception as e:
            logger.error(f"[WoL] Failed to send magic packet: {e}")
            return False

    async def check_pc_reachability(self, timeout_sec: float = 1.0) -> bool:
        """
        Checks if the PC workstation is online by attempting a TCP handshake on the agent port.
        """
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(self.pc_ip, self.pc_port),
                timeout=timeout_sec,
            )
            writer.close()
            await writer.wait_closed()
            self.is_pc_awake = True
            return True
        except Exception:
            self.is_pc_awake = False
            return False

    async def wake_and_wait(self, max_wait_sec: float = 30.0, poll_interval: float = 2.0) -> bool:
        """
        Fires the WoL packet and polls until the PC becomes reachable.
        """
        logger.info(f"[WoL] Waking PC ({self.pc_mac} / {self.pc_ip})...")
        self.send_wol_packet()

        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < max_wait_sec:
            if await self.check_pc_reachability(timeout_sec=1.0):
                logger.info("[WoL] PC is now ONLINE and responding!")
                return True
            await asyncio.sleep(poll_interval)

        logger.warning(f"[WoL] PC did not respond within {max_wait_sec} seconds.")
        return False

    async def start_monitoring(self, poll_interval_sec: float = 10.0) -> None:
        """Starts background periodic health monitoring task."""
        if self._sentinel_task and not self._sentinel_task.done():
            return

        async def _loop():
            logger.info("[WoL Sentinel] Background monitoring started.")
            while True:
                prev_state = self.is_pc_awake
                current_state = await self.check_pc_reachability(timeout_sec=1.5)
                if current_state != prev_state:
                    status_text = "ONLINE" if current_state else "OFFLINE"
                    logger.info(f"[WoL Sentinel] PC status changed to: {status_text}")
                await asyncio.sleep(poll_interval_sec)

        self._sentinel_task = asyncio.create_task(_loop())

    def stop_monitoring(self) -> None:
        """Stops the background monitoring loop."""
        if self._sentinel_task:
            self._sentinel_task.cancel()
            self._sentinel_task = None
            logger.info("[WoL Sentinel] Background monitoring stopped.")

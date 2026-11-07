"""
Vector Bridge Module.
Provides high-level abstraction over Vector 2.0 SDK.
Includes full hardware simulation (MockVectorRobot) when physical robot is not connected.
"""

from __future__ import annotations

import asyncio
import logging
import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("vector.bridge")


@dataclass
class RobotTelemetry:
    """Robot state snapshot."""
    x: float = 0.0
    y: float = 0.0
    heading_deg: float = 0.0
    head_angle_deg: float = 0.0
    lift_height: float = 0.0  # 0.0 (ground) to 1.0 (top)
    battery_volts: float = 3.95
    battery_percentage: int = 88
    is_on_charger: bool = True
    is_charging: bool = False
    is_cliff_detected: bool = False
    last_spoken_text: str = ""
    is_speaking: bool = False
    current_expression: str = "neutral"
    connected: bool = True


class MockVectorRobot:
    """
    Complete software mock simulator for Anki/DDL Vector 2.0.
    Simulates mobility, head/lift actuators, battery, sound, and face display.
    """

    def __init__(self, serial: str = "00e201a4", name: str = "Vector-SIM"):
        self.serial = serial
        self.name = name
        self.telemetry = RobotTelemetry()
        self._speech_lock = asyncio.Lock()
        logger.info(f"Initialized MockVectorRobot ({self.name}, S/N: {self.serial})")

    async def connect(self) -> bool:
        self.telemetry.connected = True
        logger.info(f"Connected to mock robot {self.name}")
        return True

    async def disconnect(self) -> None:
        self.telemetry.connected = False
        logger.info(f"Disconnected from mock robot {self.name}")

    async def drive_straight(self, distance_mm: float, speed_mmps: float = 50.0) -> bool:
        """Simulates driving forward or backward."""
        if self.telemetry.is_on_charger and distance_mm > 0:
            logger.info("Undocking robot from charger before driving forward.")
            self.telemetry.is_on_charger = False

        duration = abs(distance_mm) / max(speed_mmps, 1.0)
        # Update (x,y) coordinates based on heading
        rad = math.radians(self.telemetry.heading_deg)
        self.telemetry.x += distance_mm * math.cos(rad)
        self.telemetry.y += distance_mm * math.sin(rad)
        logger.info(
            f"[MOCK ROBOT] Drove {distance_mm:.1f} mm at {speed_mmps:.1f} mm/s. "
            f"New pos: ({self.telemetry.x:.1f}, {self.telemetry.y:.1f})"
        )
        await asyncio.sleep(min(duration * 0.1, 0.5))  # Scaled simulation time
        return True

    async def turn_in_place(self, angle_deg: float, speed_dps: float = 100.0) -> bool:
        """Simulates turning in place."""
        duration = abs(angle_deg) / max(speed_dps, 1.0)
        self.telemetry.heading_deg = (self.telemetry.heading_deg + angle_deg) % 360.0
        logger.info(
            f"[MOCK ROBOT] Turned {angle_deg:.1f}° at {speed_dps:.1f} °/s. "
            f"New heading: {self.telemetry.heading_deg:.1f}°"
        )
        await asyncio.sleep(min(duration * 0.1, 0.5))
        return True

    async def set_head_angle(self, angle_deg: float) -> bool:
        """Sets head pitch angle (safe hardware range: -22.0° to +45.0°)."""
        clamped = max(-22.0, min(45.0, angle_deg))
        self.telemetry.head_angle_deg = clamped
        logger.info(f"[MOCK ROBOT] Head angle set to {clamped:.1f}°")
        return True

    async def set_lift_height(self, height: float) -> bool:
        """Sets lift arm height (0.0=lowest to 1.0=highest)."""
        clamped = max(0.0, min(1.0, height))
        self.telemetry.lift_height = clamped
        logger.info(f"[MOCK ROBOT] Lift height set to {clamped:.2f}")
        return True

    async def say_text(self, text: str, duration_sec: Optional[float] = None) -> bool:
        """Simulates TTS speech on Vector's speaker."""
        async with self._speech_lock:
            self.telemetry.is_speaking = True
            self.telemetry.last_spoken_text = text
            # Estimate speech duration if not specified (~150 words per minute)
            est_duration = duration_sec or max(0.5, len(text.split()) * 0.4)
            logger.info(f"[MOCK ROBOT SPEAKING]: \"{text}\" (~{est_duration:.1f}s)")
            await asyncio.sleep(min(est_duration * 0.2, 1.0))
            self.telemetry.is_speaking = False
        return True

    async def play_wav(self, wav_bytes: bytes) -> bool:
        """Simulates playing raw WAV audio on Vector's speaker."""
        async with self._speech_lock:
            self.telemetry.is_speaking = True
            logger.info(f"[MOCK ROBOT AUDIO] Playing {len(wav_bytes)} bytes of WAV audio")
            await asyncio.sleep(0.3)
            self.telemetry.is_speaking = False
        return True

    async def set_face_expression(self, expression: str) -> bool:
        """Simulates changing Vector's 184x96 OLED eye expression."""
        valid_expressions = ["neutral", "happy", "sarcastic", "curious", "surprised", "sleepy", "angry"]
        if expression not in valid_expressions:
            expression = "neutral"
        self.telemetry.current_expression = expression
        logger.info(f"[MOCK ROBOT SCREEN] Eye expression set to: '{expression}'")
        return True

    async def dock_on_charger(self) -> bool:
        """Simulates driving onto the charger."""
        logger.info("[MOCK ROBOT] Navigating to charger...")
        await asyncio.sleep(0.2)
        self.telemetry.is_on_charger = True
        self.telemetry.is_charging = True
        logger.info("[MOCK ROBOT] Successfully docked on charger.")
        return True

    def get_status(self) -> Dict[str, Any]:
        """Returns structured state dictionary."""
        return {
            "name": self.name,
            "serial": self.serial,
            "connected": self.telemetry.connected,
            "x": round(self.telemetry.x, 2),
            "y": round(self.telemetry.y, 2),
            "heading_deg": round(self.telemetry.heading_deg, 2),
            "head_angle_deg": round(self.telemetry.head_angle_deg, 2),
            "lift_height": round(self.telemetry.lift_height, 2),
            "battery_volts": round(self.telemetry.battery_volts, 2),
            "battery_percentage": self.telemetry.battery_percentage,
            "is_on_charger": self.telemetry.is_on_charger,
            "is_charging": self.telemetry.is_charging,
            "is_speaking": self.telemetry.is_speaking,
            "last_spoken_text": self.telemetry.last_spoken_text,
            "current_expression": self.telemetry.current_expression,
        }


class VectorBridge:
    """
    Unified Vector Bridge adapter.
    Dispatches calls to real `wirepod-vector-sdk` when hardware is available,
    or to `MockVectorRobot` when in simulation mode.
    """

    def __init__(self, mock_mode: bool = True, serial: str = "00000000", ip: str = "127.0.0.1"):
        self.mock_mode = mock_mode
        self.serial = serial
        self.ip = ip
        self._mock_robot = MockVectorRobot(serial=serial)
        self._real_robot = None
        logger.info(f"VectorBridge initialized (mock_mode={self.mock_mode})")

    async def initialize(self) -> bool:
        if self.mock_mode:
            return await self._mock_robot.connect()

        # Physical hardware branch: attempt to import wirepod-vector-sdk
        try:
            import anki_vector
            logger.info("anki_vector SDK imported. Initializing hardware connection...")
            # Real hardware connection logic via Robot()
            self._real_robot = anki_vector.AsyncRobot(serial=self.serial, ip=self.ip)
            await self._real_robot.connect()
            logger.info(f"Connected to physical Vector 2.0 at {self.ip}")
            return True
        except ImportError:
            logger.warning(
                "wirepod-vector-sdk / anki_vector not installed. Falling back to MockVectorRobot."
            )
            self.mock_mode = True
            return await self._mock_robot.connect()
        except Exception as e:
            logger.error(f"Failed to connect to physical Vector: {e}. Falling back to mock.")
            self.mock_mode = True
            return await self._mock_robot.connect()

    async def say_text(self, text: str) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.say_text(text)
        try:
            await self._real_robot.say_text(text)
            return True
        except Exception as e:
            logger.error(f"Hardware say_text failed: {e}")
            return False

    async def drive_straight(self, distance_mm: float, speed_mmps: float = 50.0) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.drive_straight(distance_mm, speed_mmps)
        try:
            import anki_vector.util
            dist = anki_vector.util.distance_mm(distance_mm)
            spd = anki_vector.util.speed_mmps(speed_mmps)
            await self._real_robot.behavior.drive_straight(dist, spd)
            return True
        except Exception as e:
            logger.error(f"Hardware drive_straight failed: {e}")
            return False

    async def turn_in_place(self, angle_deg: float, speed_dps: float = 100.0) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.turn_in_place(angle_deg, speed_dps)
        try:
            import anki_vector.util
            ang = anki_vector.util.degrees(angle_deg)
            spd = anki_vector.util.Angle(degrees=speed_dps)
            await self._real_robot.behavior.turn_in_place(ang, spd)
            return True
        except Exception as e:
            logger.error(f"Hardware turn_in_place failed: {e}")
            return False

    async def set_head_angle(self, angle_deg: float) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.set_head_angle(angle_deg)
        try:
            import anki_vector.util
            ang = anki_vector.util.degrees(angle_deg)
            await self._real_robot.behavior.set_head_angle(ang)
            return True
        except Exception as e:
            logger.error(f"Hardware set_head_angle failed: {e}")
            return False

    async def set_lift_height(self, height: float) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.set_lift_height(height)
        try:
            await self._real_robot.behavior.set_lift_height(height)
            return True
        except Exception as e:
            logger.error(f"Hardware set_lift_height failed: {e}")
            return False

    async def play_wav(self, wav_bytes: bytes) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.play_wav(wav_bytes)
        try:
            # Stream wav to physical Vector
            import io
            stream = io.BytesIO(wav_bytes)
            await self._real_robot.audio.stream_wav_file(stream, volume=80)
            return True
        except Exception as e:
            logger.error(f"Hardware play_wav failed: {e}")
            return False

    async def set_face_expression(self, expression: str) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.set_face_expression(expression)
        return True

    async def dock_on_charger(self) -> bool:
        if self.mock_mode or not self._real_robot:
            return await self._mock_robot.dock_on_charger()
        try:
            await self._real_robot.behavior.drive_on_charger()
            return True
        except Exception as e:
            logger.error(f"Hardware dock_on_charger failed: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        if self.mock_mode or not self._real_robot:
            return self._mock_robot.get_status()
        # Physical robot status wrapper
        return {
            "name": "Vector-Physical",
            "serial": self.serial,
            "connected": True,
            "mock": False,
        }

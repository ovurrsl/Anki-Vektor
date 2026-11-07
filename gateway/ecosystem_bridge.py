"""
Ecosystem Bridge for ovurrsl's Hardware & Open-Source Repositories:
1. `ovurrsl/arduino-room-thermostat` (Arduino GIGA R1 + BME680 + UNO R4 BLE Thermostat)
   - Service UUID: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
   - Characteristics: temp_C (6E400002), setpoint_C (6E400003), relay_state (6E400004), system_mode (6E400005)
2. `ovurrsl/Dynamic-Lighting` (AmbiFlux 108-LED WS2812B Monitor Ambilight via `Awa` / `Ada` protocol)
   - Synchronizes desk ambient lighting with Vector's mood/expression and UNO Q states.
3. `jweaver60/link-studio` & `tagawa0525/insta360-link2pro-linux`
   - UVC Extension Unit 9 (`wIndex=0x0900`) hardware modes for Insta360 Link 2 (AI Tracking, Whiteboard, Overhead, DeskView, Privacy).
"""

from __future__ import annotations

import logging
import struct
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("vector.ecosystem_bridge")

# BLE UUIDs from ovurrsl/arduino-room-thermostat/docs/protocol.md
THERMOSTAT_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_TEMP_C_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_SETPOINT_C_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_RELAY_STATE_UUID = "6E400004-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_SYSTEM_MODE_UUID = "6E400005-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_HYSTERESIS_UUID = "6E400006-B5A3-F393-E0A9-E50E24DCCA9E"

SYSTEM_MODES = {
    0: "Heating",
    1: "Cooling",
    2: "Fan",
    3: "Off",
}
MODE_NAME_TO_BYTE = {v.lower(): k for k, v in SYSTEM_MODES.items()}

# AmbiFlux (`ovurrsl/Dynamic-Lighting`) mood color presets (R, G, B)
AMBIFLUX_MOOD_COLORS: Dict[str, Tuple[int, int, int]] = {
    "neutral": (0, 170, 255),     # Vector Cyan
    "happy": (16, 185, 129),      # Emerald Green
    "curious": (168, 85, 247),    # Purple
    "thinking": (59, 130, 246),   # Deep Blue
    "sarcastic": (245, 158, 11),  # Amber
    "angry": (239, 68, 68),       # Crimson Red
    "sleepy": (30, 41, 59),       # Dim Slate
    "wake_pc": (34, 211, 238),    # Bright Electric Cyan
}


class RoomThermostatBridge:
    """
    Connects Arduino UNO Q (built-in BLE) to `ovurrsl/arduino-room-thermostat`
    (Arduino GIGA R1 BME680 + UNO R4 Relay Node).
    """

    def __init__(self):
        self.temp_c: float = 22.4
        self.setpoint_c: float = 23.0
        self.humidity_pct: float = 44.5
        self.iaq_ohms: int = 128000
        self.relay_on: bool = True
        self.system_mode: int = 0  # 0 = Heating
        self.hysteresis_c: float = 0.5

    @staticmethod
    def encode_float32_le(value: float) -> bytes:
        """Encodes float as IEEE 754 4-byte little-endian payload per protocol.md."""
        return struct.pack("<f", float(value))

    @staticmethod
    def decode_float32_le(payload: bytes) -> float:
        """Decodes 4-byte IEEE 754 float payload from GIGA R1 / UNO R4."""
        if len(payload) != 4:
            raise ValueError("BLE float32 payload must be exactly 4 bytes")
        return round(struct.unpack("<f", payload)[0], 2)

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns current room climate telemetry and BLE characteristics."""
        return {
            "repo": "ovurrsl/arduino-room-thermostat",
            "service_uuid": THERMOSTAT_SERVICE_UUID,
            "temp_c": self.temp_c,
            "setpoint_c": self.setpoint_c,
            "humidity_pct": self.humidity_pct,
            "iaq_ohms": self.iaq_ohms,
            "relay_state": "ON" if self.relay_on else "OFF",
            "system_mode": SYSTEM_MODES.get(self.system_mode, "Off"),
            "hysteresis_c": self.hysteresis_c,
            "summary_tr": (
                f"Oda sıcaklığı {self.temp_c:.1f} derece, hedef sıcaklık {self.setpoint_c:.1f} derece. "
                f"Mod: {SYSTEM_MODES.get(self.system_mode, 'Off')}, Röle: {'AÇIK' if self.relay_on else 'KAPALI'}."
            ),
        }

    def set_target_temperature(self, setpoint_c: float, mode: str = "heating") -> Dict[str, Any]:
        """Updates target setpoint and recalculates hysteresis relay state."""
        self.setpoint_c = round(max(10.0, min(35.0, float(setpoint_c))), 1)
        mode_key = mode.strip().lower()
        if mode_key in MODE_NAME_TO_BYTE:
            self.system_mode = MODE_NAME_TO_BYTE[mode_key]

        # Apply hysteresis logic from `firmware/uno_relay_node`
        if self.system_mode == 0:  # Heating
            if self.temp_c <= (self.setpoint_c - self.hysteresis_c):
                self.relay_on = True
            elif self.temp_c >= (self.setpoint_c + self.hysteresis_c):
                self.relay_on = False
        elif self.system_mode == 3:  # Off
            self.relay_on = False

        return self.get_telemetry()


class AmbiFluxBridge:
    """
    Implements the serial frame generator from `ovurrsl/Dynamic-Lighting` (`lib/engine/protocol.ts`)
    to drive the 108-LED WS2812B monitor ambilight strip in sync with Vector's emotions.
    """

    HEADER_XOR = 0x55

    def __init__(self, led_count: int = 108):
        self.led_count = max(1, min(65536, led_count))
        self.current_mood = "neutral"
        self.current_rgb: Tuple[int, int, int] = AMBIFLUX_MOOD_COLORS["neutral"]

    @staticmethod
    def compute_fletcher_trailer(payload: bytes) -> bytes:
        """Computes the 3-byte Fletcher checksum trailer used by `Awa` frames in Dynamic-Lighting."""
        sum1 = 0
        sum2 = 0
        for b in payload:
            sum1 = (sum1 + b) % 255
            sum2 = (sum2 + sum1) % 255
        chk = (255 - ((sum1 + sum2) % 255)) % 255
        return bytes([sum1, sum2, chk])

    def build_awa_frame(self, r: int, g: int, b: int) -> bytes:
        """
        Builds a binary `Awa` frame compatible with `FrameParser` in `ovurrsl/Dynamic-Lighting/lib/engine/protocol.ts`.
        Header: 'A', 'w', 'a', HI, LO, (HI ^ LO ^ 0x55)
        Payload: N * 3 bytes (R, G, B)
        Trailer: 3-byte Fletcher checksum
        """
        count_minus_one = self.led_count - 1
        hi = (count_minus_one >> 8) & 0xFF
        lo = count_minus_one & 0xFF
        chk = hi ^ lo ^ self.HEADER_XOR
        header = bytes([ord("A"), ord("w"), ord("a"), hi, lo, chk])
        payload = bytes([r & 0xFF, g & 0xFF, b & 0xFF]) * self.led_count
        trailer = self.compute_fletcher_trailer(payload)
        return header + payload + trailer

    def set_mood_lighting(self, mood: str) -> Dict[str, Any]:
        """Sets the 108-LED AmbiFlux monitor backlight to match Vector's mood."""
        key = mood.strip().lower()
        rgb = AMBIFLUX_MOOD_COLORS.get(key, AMBIFLUX_MOOD_COLORS["neutral"])
        self.current_mood = key if key in AMBIFLUX_MOOD_COLORS else "neutral"
        self.current_rgb = rgb
        frame = self.build_awa_frame(*rgb)
        return {
            "repo": "ovurrsl/Dynamic-Lighting",
            "protocol": "Awa",
            "led_count": self.led_count,
            "mood": self.current_mood,
            "rgb": list(rgb),
            "frame_byte_length": len(frame),
            "header_hex": frame[:6].hex(),
        }

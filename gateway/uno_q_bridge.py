"""
Arduino UNO Q (ABX00173) Dual-Brain Hardware Bridge.
Communicates between the Qualcomm Dragonwing QRB2210 Linux MPU (or Windows Local PC)
and the STM32U585 Cortex-M33 MCU (8x13 Blue LED Matrix & real-time GPIO).

Supports three automatic transport layers:
1. Native ArduinoBridge RPC (`arduino_bridge` Python package on UNO Q Debian OS).
2. Direct USB Serial via `pyserial` (`COM*` on Windows, `/dev/ttyACM*` or `/dev/ttyHS1` on Linux).
3. High-fidelity In-Memory Simulation (when running without serial port attached).
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

logger = logging.getLogger("vector.uno_q_bridge")

try:
    import serial
    import serial.tools.list_ports

    PYSERIAL_AVAILABLE = True
except ImportError:
    PYSERIAL_AVAILABLE = False

VALID_STATUS_PATTERNS = {
    "IDLE": [
        "0000000000000",
        "0000111000000",
        "0001100000000",
        "0011000000000",
        "0011000000000",
        "0001100000000",
        "0000111000000",
        "0000000000000",
    ],
    "LISTENING": [
        "0000011100000",
        "0000100010000",
        "0000100010000",
        "0000100010000",
        "0000011100000",
        "0001001001000",
        "0000111110000",
        "0000001000000",
    ],
    "THINKING": [
        "0000001000000",
        "0001001001000",
        "0101001001010",
        "0101011101010",
        "0101011101010",
        "0101001001010",
        "0001001001000",
        "0000001000000",
    ],
    "WAKE_PC": [
        "0011111111100",
        "0010000000100",
        "0010110110100",
        "0010000000100",
        "0010011100100",
        "0011111111100",
        "0000011100000",
        "0000111110000",
    ],
    "VECTOR_OK": [
        "0011000001100",
        "0011000001100",
        "0001100011000",
        "0001100011000",
        "0000110110000",
        "0000110110000",
        "0000011100000",
        "0000001000000",
    ],
    "ERROR": [
        "0010000000100",
        "0001000001000",
        "0000100010000",
        "0000011100000",
        "0000011100000",
        "0000100010000",
        "0001000001000",
        "0010000000100",
    ],
}

STATE_TO_NUMERIC_CODE = {
    "IDLE": 1,
    "STANDBY": 1,
    "WAKE_PC": 2,
    "PC_ON": 2,
    "LISTENING": 3,
    "THINKING": 4,
    "SPEAKING": 4,
    "VECTOR_OK": 5,
    "ERROR": 9,
}


class UnoQBridge:
    """Manages Dual-Brain RPC and LED Matrix states on Arduino UNO Q (ABX00173)."""

    def __init__(self, serial_port: Optional[str] = None, baudrate: int = 115200):
        self.serial_port = serial_port or os.getenv("UNO_Q_SERIAL_PORT", "")
        self.baudrate = baudrate
        self.current_state: str = "WAKE_PC"
        self.transport_mode: str = "SIMULATION"
        self._rpc_client: Any = None
        self._detect_transport()

    @staticmethod
    def list_available_serial_ports() -> List[Dict[str, str]]:
        """Scans all Windows COM* and Linux /dev/tty* ports via pyserial."""
        if not PYSERIAL_AVAILABLE:
            return []
        ports = []
        for p in serial.tools.list_ports.comports():
            ports.append(
                {
                    "device": p.device,
                    "description": p.description or "",
                    "hwid": p.hwid or "",
                }
            )
        return ports

    def _detect_transport(self) -> None:
        """Detects whether we are running on real UNO Q Linux or connected via Windows/Linux USB Serial."""
        try:
            import arduino_bridge  # type: ignore

            self._rpc_client = arduino_bridge.BridgeClient()
            self.transport_mode = "ARDUINO_BRIDGE_RPC"
            logger.info("Connected to STM32U585 via native ArduinoBridge RPC.")
            return
        except ImportError:
            pass

        # Auto-discover via pyserial (works on Windows COM3, COM4, etc. and Linux /dev/ttyACM0)
        if PYSERIAL_AVAILABLE and not self.serial_port:
            available = self.list_available_serial_ports()
            for p in available:
                desc = (p["description"] + " " + p["hwid"]).lower()
                if any(k in desc for k in ("arduino", "stm32", "usb", "acm", "qualcomm", "com")):
                    self.serial_port = p["device"]
                    self.transport_mode = "SERIAL_BRIDGE"
                    logger.info(f"Auto-detected Arduino UNO Q on serial port: {self.serial_port} ({p['description']})")
                    return

        # Fallback path check
        candidate_ports = (
            [self.serial_port]
            if self.serial_port
            else ["/dev/ttyHS1", "/dev/ttyACM0", "/dev/ttyUSB0"]
        )
        for port in candidate_ports:
            if port and (os.path.exists(port) or port.upper().startswith("COM")):
                self.serial_port = port
                self.transport_mode = "SERIAL_BRIDGE"
                logger.info(f"Configured UNO Q serial device at {port}")
                return

        self.transport_mode = "SIMULATION"
        logger.info("UNO Q STM32U585 Bridge running in simulation mode (no USB COM port found yet).")

    def set_led_status(self, state: str, override_port: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates the 8x13 Blue LED Matrix on the STM32U585 MCU.
        Valid states: IDLE, LISTENING, THINKING, WAKE_PC, VECTOR_OK, ERROR.
        """
        if override_port:
            self.serial_port = override_port
            self.transport_mode = "SERIAL_BRIDGE"

        raw = state.strip().upper()
        if raw in ("1", "STANDBY"):
            normalized = "IDLE"
        elif raw in ("2", "PC_ON"):
            normalized = "WAKE_PC"
        elif raw == "3":
            normalized = "LISTENING"
        elif raw in ("4", "SPEAKING"):
            normalized = "THINKING"
        elif raw in ("5", "VECTOR"):
            normalized = "VECTOR_OK"
        elif raw in VALID_STATUS_PATTERNS:
            normalized = raw
        else:
            normalized = "ERROR"

        self.current_state = normalized
        num_code = STATE_TO_NUMERIC_CODE.get(normalized, 2)

        if self.transport_mode == "ARDUINO_BRIDGE_RPC" and self._rpc_client is not None:
            try:
                self._rpc_client.call("set_status", num_code)
            except Exception as e:
                logger.warning(f"ArduinoBridge RPC call failed: {e}")

        elif self.transport_mode == "SERIAL_BRIDGE" and self.serial_port:
            try:
                if PYSERIAL_AVAILABLE:
                    with serial.Serial(self.serial_port, self.baudrate, timeout=1.0) as ser:
                        ser.write(f"SET_STATUS:{num_code}\n".encode("utf-8"))
                        ser.flush()
                else:
                    with open(self.serial_port, "w", encoding="utf-8") as f:
                        f.write(f"SET_STATUS:{num_code}\n")
            except Exception as e:
                logger.warning(f"Serial write to {self.serial_port} failed: {e}")

        return {
            "state": self.current_state,
            "numeric_code": num_code,
            "transport": self.transport_mode,
            "serial_port": self.serial_port or "none",
            "matrix_bitmap": VALID_STATUS_PATTERNS[self.current_state],
        }

    def get_status(self) -> Dict[str, Any]:
        """Returns current STM32U585 MCU status, detected COM ports, and 8x13 bitmap."""
        return {
            "board": "Arduino UNO Q 4GB (ABX00173)",
            "mpu": "Qualcomm Dragonwing QRB2210",
            "mcu": "STM32U585 Cortex-M33",
            "transport": self.transport_mode,
            "serial_port": self.serial_port or "auto",
            "available_ports": self.list_available_serial_ports(),
            "led_state": self.current_state,
            "matrix_bitmap": VALID_STATUS_PATTERNS.get(
                self.current_state, VALID_STATUS_PATTERNS["WAKE_PC"]
            ),
        }

    def compile_and_flash_sketch(
        self,
        sketch_path: str = "mcu_sketch/uno_q_status_matrix.ino",
        fqbn: str = "arduino:stm32:uno_q",
        port: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Uses `arduino-cli` (system PATH or `.tools/arduino-cli/arduino-cli.exe`)
        to compile and upload the STM32U585 LED matrix sketch on the local PC.
        """
        target_port = port or self.serial_port
        cli_bin = shutil.which("arduino-cli")
        if not cli_bin:
            local_win_cli = os.path.join(".tools", "arduino-cli", "arduino-cli.exe")
            if os.path.exists(local_win_cli):
                cli_bin = local_win_cli

        if not cli_bin:
            return {
                "status": "skipped",
                "reason": "arduino-cli not found. Run CALISTIR_LOCAL.bat on your Windows PC to auto-download it.",
                "sketch": sketch_path,
            }

        try:
            compile_cmd = [cli_bin, "compile", "--fqbn", fqbn, sketch_path]
            res_compile = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=90
            )
            if res_compile.returncode != 0:
                return {
                    "status": "compile_error",
                    "stderr": res_compile.stderr.strip(),
                }

            upload_cmd = [cli_bin, "upload", "--fqbn", fqbn, sketch_path]
            if target_port:
                upload_cmd.extend(["-p", target_port])

            res_upload = subprocess.run(
                upload_cmd, capture_output=True, text=True, timeout=90
            )
            return {
                "status": "ok" if res_upload.returncode == 0 else "upload_error",
                "port": target_port,
                "stdout": res_upload.stdout.strip(),
                "stderr": res_upload.stderr.strip(),
            }
        except Exception as e:
            return {"status": "error", "reason": str(e)}

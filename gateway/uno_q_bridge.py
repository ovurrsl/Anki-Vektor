"""
Arduino UNO Q (ABX00173) Dual-Brain Hardware Bridge.
Communicates between the Qualcomm Dragonwing QRB2210 Linux MPU and the
STM32U585 Cortex-M33 MCU (8x13 Blue LED Matrix & real-time GPIO).

Supports three automatic transport layers:
1. Native ArduinoBridge RPC (`arduino_bridge` Python package on UNO Q Debian OS).
2. Direct Serial RPC over `/dev/ttyACM0`, `/dev/ttyHS1`, or Windows `COM*` ports.
3. High-fidelity In-Memory Simulation (when running on PC without serial port attached).
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

logger = logging.getLogger("vector.uno_q_bridge")

VALID_STATUS_PATTERNS = {
    "IDLE": [
        "0000000000000",
        "0001100011000",
        "0001100011000",
        "0000000000000",
        "0000000000000",
        "0001000001000",
        "0000111110000",
        "0000000000000",
    ],
    "LISTENING": [
        "0000001000000",
        "0000101010000",
        "0010101010100",
        "1010101010101",
        "1010101010101",
        "0010101010100",
        "0000101010000",
        "0000001000000",
    ],
    "THINKING": [
        "0000111110000",
        "0001000001000",
        "0010011100100",
        "0010100010100",
        "0010100010100",
        "0010011100100",
        "0001000001000",
        "0000111110000",
    ],
    "WAKE_PC": [
        "0000011100000",
        "0000111000000",
        "0001110000000",
        "0011111111000",
        "0000001110000",
        "0000011100000",
        "0000111000000",
        "0001100000000",
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


class UnoQBridge:
    """Manages Dual-Brain RPC and LED Matrix states on Arduino UNO Q (ABX00173)."""

    def __init__(self, serial_port: Optional[str] = None):
        self.serial_port = serial_port or os.getenv("UNO_Q_SERIAL_PORT", "")
        self.current_state: str = "IDLE"
        self.transport_mode: str = "SIMULATION"
        self._rpc_client: Any = None
        self._detect_transport()

    def _detect_transport(self) -> None:
        """Detects whether we are running on real UNO Q Linux or connected via USB Serial."""
        try:
            import arduino_bridge  # type: ignore

            self._rpc_client = arduino_bridge.BridgeClient()
            self.transport_mode = "ARDUINO_BRIDGE_RPC"
            logger.info("Connected to STM32U585 via native ArduinoBridge RPC.")
            return
        except ImportError:
            pass

        # Check common Linux/Windows serial device nodes
        candidate_ports = (
            [self.serial_port]
            if self.serial_port
            else ["/dev/ttyHS1", "/dev/ttyACM0", "/dev/ttyUSB0"]
        )
        for port in candidate_ports:
            if port and os.path.exists(port):
                self.serial_port = port
                self.transport_mode = "SERIAL_BRIDGE"
                logger.info(f"Detected UNO Q serial device at {port}")
                return

        self.transport_mode = "SIMULATION"
        logger.info("UNO Q STM32U585 Bridge running in high-fidelity simulation mode.")

    def set_led_status(self, state: str) -> Dict[str, Any]:
        """
        Updates the 8x13 Blue LED Matrix on the STM32U585 MCU.
        Valid states: IDLE, LISTENING, THINKING, WAKE_PC, ERROR.
        """
        normalized = state.strip().upper()
        if normalized not in VALID_STATUS_PATTERNS:
            normalized = "ERROR"

        self.current_state = normalized

        if self.transport_mode == "ARDUINO_BRIDGE_RPC" and self._rpc_client is not None:
            try:
                self._rpc_client.call("set_status", normalized)
            except Exception as e:
                logger.warning(f"ArduinoBridge RPC call failed: {e}")

        elif self.transport_mode == "SERIAL_BRIDGE" and self.serial_port:
            try:
                with open(self.serial_port, "w", encoding="utf-8") as f:
                    f.write(f"set_status:{normalized}\n")
            except Exception as e:
                logger.warning(f"Serial write to {self.serial_port} failed: {e}")

        return {
            "state": self.current_state,
            "transport": self.transport_mode,
            "matrix_bitmap": VALID_STATUS_PATTERNS[self.current_state],
        }

    def get_status(self) -> Dict[str, Any]:
        """Returns current STM32U585 MCU status and 8x13 bitmap."""
        return {
            "board": "Arduino UNO Q 4GB (ABX00173)",
            "mpu": "Qualcomm Dragonwing QRB2210",
            "mcu": "STM32U585 Cortex-M33",
            "transport": self.transport_mode,
            "serial_port": self.serial_port or "auto",
            "led_state": self.current_state,
            "matrix_bitmap": VALID_STATUS_PATTERNS.get(
                self.current_state, VALID_STATUS_PATTERNS["IDLE"]
            ),
        }

    def compile_and_flash_sketch(
        self,
        sketch_path: str = "mcu_sketch/uno_q_status_matrix.ino",
        fqbn: str = "arduino:stm32:uno_q",
    ) -> Dict[str, Any]:
        """
        Uses `arduino-cli` (if installed on host or UNO Q) to compile and upload
        the STM32U585 LED matrix sketch.
        """
        cli_bin = shutil.which("arduino-cli")
        if not cli_bin:
            return {
                "status": "skipped",
                "reason": "arduino-cli not found in PATH. Run scripts/auto_setup_windows_and_uno_q.ps1 on your PC.",
                "sketch": sketch_path,
            }

        try:
            compile_cmd = [cli_bin, "compile", "--fqbn", fqbn, sketch_path]
            res_compile = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=60
            )
            if res_compile.returncode != 0:
                return {
                    "status": "compile_error",
                    "stderr": res_compile.stderr.strip(),
                }

            upload_cmd = [cli_bin, "upload", "--fqbn", fqbn, sketch_path]
            if self.serial_port:
                upload_cmd.extend(["-p", self.serial_port])

            res_upload = subprocess.run(
                upload_cmd, capture_output=True, text=True, timeout=60
            )
            return {
                "status": "ok" if res_upload.returncode == 0 else "upload_error",
                "stdout": res_upload.stdout.strip(),
                "stderr": res_upload.stderr.strip(),
            }
        except Exception as e:
            return {"status": "error", "reason": str(e)}

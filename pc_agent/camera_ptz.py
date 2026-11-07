"""
Insta360 Link 2 Camera & Gimbal Controller Module.
Implements UVC PTZ controls in arcseconds (1° = 3600 arcseconds, step=3600).
Includes MockCamera with dynamic desk rendering for simulation mode.
"""

from __future__ import annotations

import io
import logging
import subprocess
import time
from datetime import datetime
from typing import Optional, Tuple

logger = logging.getLogger("vector.camera")

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


def round_to_arcsec_step(value: int, step: int = 3600) -> int:
    """Insta360 Link 2 hardware only accepts exact multiples of 3600 arcseconds."""
    return int(round(value / step) * step)


class Insta360Link2Controller:
    """
    Physical controller for Insta360 Link 2 (USB ID 2e1a:4c04) over Linux V4L2/UVC.
    Safe mechanical limits:
      Pan:  -480,000 to +480,000 arcsec (±133.3°)
      Tilt: -300,000 to +320,000 arcsec (-83.3° to +88.8°)
    Supports Link Studio UVC Extension Unit 9 hardware modes:
      normal, ai_tracking, whiteboard, overhead, deskview, privacy
    """

    USB_VID_PID = "2e1a:4c04"
    UVC_XU_UNIT_ID = 0x09
    MIN_PAN = -480000
    MAX_PAN = 480000
    MIN_TILT = -300000
    MAX_TILT = 320000
    VALID_MODES = ("normal", "ai_tracking", "whiteboard", "overhead", "deskview", "privacy")

    def __init__(self, device: str = "/dev/video0"):
        self.device = device
        self.current_pan = 0
        self.current_tilt = 0
        self.current_mode = "normal"

    def set_ptz(self, pan_arcsec: int, tilt_arcsec: int) -> bool:
        """Sets absolute Pan and Tilt gimbal angles in arcseconds."""
        # Quantize to 3600 step
        pan_q = round_to_arcsec_step(pan_arcsec)
        tilt_q = round_to_arcsec_step(tilt_arcsec)

        # Clamp to hardware safe bounds
        pan_clamped = max(self.MIN_PAN, min(self.MAX_PAN, pan_q))
        tilt_clamped = max(self.MIN_TILT, min(self.MAX_TILT, tilt_q))

        try:
            # Set Pan
            subprocess.run(
                ["v4l2-ctl", "-d", self.device, "--set-ctrl", f"pan_absolute={pan_clamped}"],
                check=True,
                capture_output=True,
            )
            # Set Tilt
            subprocess.run(
                ["v4l2-ctl", "-d", self.device, "--set-ctrl", f"tilt_absolute={tilt_clamped}"],
                check=True,
                capture_output=True,
            )
            self.current_pan = pan_clamped
            self.current_tilt = tilt_clamped
            logger.info(f"Insta360 Link 2 PTZ set to Pan={pan_clamped}, Tilt={tilt_clamped}")
            return True
        except Exception as e:
            logger.error(f"Failed to set Insta360 Link 2 PTZ via v4l2-ctl: {e}")
            return False

    def set_desk_view(self) -> bool:
        """Points camera down at desk surface (-80° = -288000 arcsec)."""
        self.current_mode = "deskview"
        return self.set_ptz(pan_arcsec=0, tilt_arcsec=-288000)

    def set_hardware_mode(self, mode: str) -> bool:
        """Switches Insta360 Link 2 hardware gimbal/AI mode (inspired by jweaver60/link-studio)."""
        m = mode.strip().lower()
        if m not in self.VALID_MODES:
            return False
        self.current_mode = m
        if m == "deskview":
            return self.set_ptz(0, -288000)
        if m == "overhead":
            return self.set_ptz(0, -300000)
        if m == "privacy":
            return self.set_ptz(0, -300000)
        if m == "normal":
            return self.set_ptz(0, 0)
        return True

    def capture_frame(self) -> bytes:
        """Captures a single frame from the camera using fswebcam or ffmpeg."""
        try:
            proc = subprocess.run(
                ["fswebcam", "-d", self.device, "-r", "1920x1080", "--no-banner", "-"],
                capture_output=True,
                check=True,
            )
            return proc.stdout
        except Exception as e:
            logger.error(f"Physical camera frame capture failed: {e}")
            return b""


class MockCamera:
    """
    Virtual camera simulator for desktop environment.
    Generates dynamic 1280x720 JPEG images depicting the desk, Vector robot, and camera telemetry.
    """

    VALID_MODES = Insta360Link2Controller.VALID_MODES

    def __init__(self):
        self.current_pan = 0
        self.current_tilt = 0
        self.current_mode = "normal"

    def set_ptz(self, pan_arcsec: int, tilt_arcsec: int) -> bool:
        pan_q = round_to_arcsec_step(pan_arcsec)
        tilt_q = round_to_arcsec_step(tilt_arcsec)
        self.current_pan = max(-480000, min(480000, pan_q))
        self.current_tilt = max(-300000, min(320000, tilt_q))
        logger.info(
            f"[MOCK CAMERA] PTZ moved to Pan={self.current_pan} arcsec ({self.current_pan/3600:.1f}°), "
            f"Tilt={self.current_tilt} arcsec ({self.current_tilt/3600:.1f}°)"
        )
        return True

    def set_desk_view(self) -> bool:
        self.current_mode = "deskview"
        return self.set_ptz(pan_arcsec=0, tilt_arcsec=-288000)

    def set_hardware_mode(self, mode: str) -> bool:
        m = mode.strip().lower()
        if m not in self.VALID_MODES:
            return False
        self.current_mode = m
        if m == "deskview":
            return self.set_ptz(0, -288000)
        if m in ("overhead", "privacy"):
            return self.set_ptz(0, -300000)
        if m == "normal":
            return self.set_ptz(0, 0)
        return True

    def capture_frame(self, robot_x: float = 0.0, robot_y: float = 0.0) -> bytes:
        """Renders and returns dynamic JPEG image bytes."""
        width, height = 1280, 720
        pan_deg = self.current_pan / 3600.0
        tilt_deg = self.current_tilt / 3600.0

        if not PILLOW_AVAILABLE:
            # Fallback simple 1x1 black JPEG if PIL not present
            return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"

        # Create dark modern workstation canvas
        img = Image.new("RGB", (width, height), color=(20, 24, 33))
        draw = ImageDraw.Draw(img)

        # Draw Desk Mat Grid
        mat_x0, mat_y0 = 140, 100
        mat_x1, mat_y1 = width - 140, height - 80
        draw.rectangle([mat_x0, mat_y0, mat_x1, mat_y1], fill=(30, 36, 48), outline=(60, 75, 100), width=2)

        # Draw grid lines
        for x in range(mat_x0 + 50, mat_x1, 50):
            draw.line([(x, mat_y0), (x, mat_y1)], fill=(40, 50, 68), width=1)
        for y in range(mat_y0 + 50, mat_y1, 50):
            draw.line([(mat_x0, y), (mat_x1, y)], fill=(40, 50, 68), width=1)

        # Draw Charger Base
        charger_cx, charger_cy = mat_x0 + 120, mat_y0 + 120
        draw.rectangle(
            [charger_cx - 40, charger_cy - 40, charger_cx + 40, charger_cy + 40],
            fill=(45, 55, 72),
            outline=(100, 120, 160),
            width=2,
        )
        draw.text((charger_cx - 30, charger_cy - 10), "CHARGER", fill=(140, 160, 190))

        # Draw Simulated Vector Robot
        rx = charger_cx + int(robot_x)
        ry = charger_cy + int(robot_y)
        # Robot Body
        draw.rectangle([rx - 30, ry - 30, rx + 30, ry + 30], fill=(15, 15, 18), outline=(0, 220, 130), width=3)
        # Head / Screen
        draw.rectangle([rx - 20, ry - 20, rx + 20, ry + 10], fill=(0, 0, 0))
        # Eyes
        draw.ellipse([rx - 14, ry - 14, rx - 4, ry - 2], fill=(0, 230, 140))
        draw.ellipse([rx + 4, ry - 14, rx + 14, ry - 2], fill=(0, 230, 140))
        # Treads
        draw.rectangle([rx - 36, ry - 28, rx - 30, ry + 28], fill=(60, 60, 65))
        draw.rectangle([rx + 30, ry - 28, rx + 36, ry + 28], fill=(60, 60, 65))
        draw.text((rx - 25, ry + 34), f"Vector ({robot_x:.0f}, {robot_y:.0f})", fill=(0, 255, 160))

        # Overlay Camera HUD & Telemetry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hud_text = (
            f"INSTA360 LINK 2 [MOCK HUD]  |  {timestamp}\n"
            f"GIMBAL: Pan={pan_deg:+.1f}° ({self.current_pan} arcsec) | "
            f"Tilt={tilt_deg:+.1f}° ({self.current_tilt} arcsec)\n"
            f"MODE: {'DESK VIEW (90° DOWN)' if tilt_deg <= -75 else 'ROOM TRACKING'}"
        )
        draw.rectangle([20, 20, 520, 95], fill=(0, 0, 0, 180), outline=(0, 180, 255), width=2)
        draw.text((32, 28), hud_text, fill=(200, 230, 255))

        # Save to buffer
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return buf.getvalue()

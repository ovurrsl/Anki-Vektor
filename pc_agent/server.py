"""
FastAPI Server & Web Dashboard for PC Workstation (RTX 5070 + Intel NPU).
Hosts REST APIs, FastMCP SSE endpoint, and serves the Web Dashboard.
"""

from __future__ import annotations

import io
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

from gateway.ecosystem_bridge import AmbiFluxBridge, RoomThermostatBridge
from gateway.uno_q_bridge import UnoQBridge
from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel
from pc_agent.camera_ptz import Insta360Link2Controller, MockCamera
from pc_agent.config import pc_config
from pc_agent.llm_router import LLMRouter
from pc_agent.npu_engine import IntelNPUEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("vector.pc_agent")

app = FastAPI(title="Vector PC Workstation Agent (RTX 5070 + NPU)", version="1.2.0")

# Workstation components
if pc_config.mock_camera:
    camera = MockCamera()
else:
    camera = Insta360Link2Controller(device=f"/dev/video{pc_config.camera_device_index}")

npu_engine = IntelNPUEngine()
llm_router = LLMRouter()
# Local bridge instance for mock robot simulation
local_vector_bridge = VectorBridge(mock_mode=True)
local_wol_sentinel = WakeOnLanSentinel()
local_uno_q_bridge = UnoQBridge()
local_thermostat = RoomThermostatBridge()
local_ambiflux = AmbiFluxBridge()


# Models
class PTZRequest(BaseModel):
    pan_arcsec: int
    tilt_arcsec: int


class CameraModeRequest(BaseModel):
    mode: str


class LedStateRequest(BaseModel):
    state: str
    port: Optional[str] = None


class FlashSketchRequest(BaseModel):
    port: Optional[str] = None
    fqbn: str = "arduino:stm32:uno_q"


class ThermostatRequest(BaseModel):
    setpoint_c: float
    mode: str = "heating"


class AmbiFluxRequest(BaseModel):
    mood: str


class DriveRequest(BaseModel):
    distance_mm: float
    speed_mmps: float = 50.0


class TurnRequest(BaseModel):
    angle_deg: float
    speed_dps: float = 100.0


class HeadRequest(BaseModel):
    angle_deg: float


class LiftRequest(BaseModel):
    height: float


class SayRequest(BaseModel):
    text: str


class ExpressionRequest(BaseModel):
    expression: str


class ChatRequest(BaseModel):
    prompt: str


class CodingRequest(BaseModel):
    task_prompt: str


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Serves the interactive web dashboard."""
    template_path = Path(__file__).parent / "templates" / "dashboard.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return "<h1>Dashboard template not found</h1>"


@app.get("/api/v1/status")
async def get_status():
    """Returns combined status of Workstation, Camera, NPU, UNO Q, Thermostat, AmbiFlux, and Vector."""
    robot_status = local_vector_bridge.get_status()
    npu_status = npu_engine.get_telemetry()
    return {
        "status": "ONLINE",
        "node": "PC Workstation (RTX 5070 + Intel NPU)",
        "robot": robot_status,
        "uno_q": local_uno_q_bridge.get_status(),
        "thermostat": local_thermostat.get_telemetry(),
        "ambiflux": local_ambiflux.set_mood_lighting(local_ambiflux.current_mood),
        "camera": {
            "mock": pc_config.mock_camera,
            "mode": getattr(camera, "current_mode", "normal"),
            "current_pan_arcsec": camera.current_pan,
            "current_tilt_arcsec": camera.current_tilt,
            "current_pan_deg": round(camera.current_pan / 3600.0, 1),
            "current_tilt_deg": round(camera.current_tilt / 3600.0, 1),
        },
        "npu": npu_status,
    }


@app.get("/api/v1/uno-q/ports")
async def get_uno_q_ports():
    """Scans local Windows COM* and Linux /dev/tty* ports for connected Arduino UNO Q."""
    local_uno_q_bridge._detect_transport()
    return {
        "active_port": local_uno_q_bridge.serial_port,
        "transport": local_uno_q_bridge.transport_mode,
        "ports": local_uno_q_bridge.list_available_serial_ports(),
    }


@app.post("/api/v1/uno-q/led")
async def set_uno_q_led(req: LedStateRequest):
    """Sets the Arduino UNO Q STM32U585 8x13 Blue LED Matrix pattern (and writes to COM port if connected)."""
    return local_uno_q_bridge.set_led_status(req.state, override_port=req.port)


@app.post("/api/v1/uno-q/flash")
async def flash_uno_q_sketch(req: FlashSketchRequest):
    """Compiles and uploads mcu_sketch/uno_q_status_matrix.ino to the locally connected Arduino UNO Q."""
    return local_uno_q_bridge.compile_and_flash_sketch(fqbn=req.fqbn, port=req.port)


@app.post("/api/v1/ecosystem/thermostat")
async def set_thermostat(req: ThermostatRequest):
    """Updates target temperature and mode on ovurrsl/arduino-room-thermostat."""
    return local_thermostat.set_target_temperature(req.setpoint_c, req.mode)


@app.post("/api/v1/ecosystem/ambiflux")
async def set_ambiflux(req: AmbiFluxRequest):
    """Updates 108-LED WS2812B monitor ambilight mood (ovurrsl/Dynamic-Lighting)."""
    return local_ambiflux.set_mood_lighting(req.mood)


@app.post("/api/v1/camera/mode")
async def set_camera_mode(req: CameraModeRequest):
    """Sets Insta360 Link 2 UVC hardware mode (normal, ai_tracking, whiteboard, overhead, deskview, privacy)."""
    success = camera.set_hardware_mode(req.mode)
    return {"status": "ok" if success else "failed", "mode": getattr(camera, "current_mode", "normal")}


@app.get("/api/v1/camera/snapshot")
async def get_camera_snapshot():
    """Returns latest JPEG image frame from Insta360 Link 2 or MockCamera."""
    status = local_vector_bridge.get_status()
    if isinstance(camera, MockCamera):
        jpeg_bytes = camera.capture_frame(robot_x=status["x"], robot_y=status["y"])
    else:
        jpeg_bytes = camera.capture_frame()

    return Response(content=jpeg_bytes, media_type="image/jpeg")


@app.post("/api/v1/camera/ptz")
async def set_camera_ptz(req: PTZRequest):
    """Sets absolute Pan/Tilt angles in arcseconds (step=3600)."""
    success = camera.set_ptz(req.pan_arcsec, req.tilt_arcsec)
    return {
        "status": "ok" if success else "failed",
        "pan_arcsec": camera.current_pan,
        "tilt_arcsec": camera.current_tilt,
    }


@app.post("/api/v1/camera/deskview")
async def set_camera_deskview():
    """Points camera straight down at desk (-80° = -288000 arcsec)."""
    success = camera.set_desk_view()
    return {"status": "ok" if success else "failed", "tilt_arcsec": camera.current_tilt}


@app.post("/api/v1/robot/drive")
async def drive_robot(req: DriveRequest):
    success = await local_vector_bridge.drive_straight(req.distance_mm, req.speed_mmps)
    return {"status": "ok" if success else "failed", "telemetry": local_vector_bridge.get_status()}


@app.post("/api/v1/robot/turn")
async def turn_robot(req: TurnRequest):
    success = await local_vector_bridge.turn_in_place(req.angle_deg, req.speed_dps)
    return {"status": "ok" if success else "failed", "telemetry": local_vector_bridge.get_status()}


@app.post("/api/v1/robot/head")
async def set_head(req: HeadRequest):
    success = await local_vector_bridge.set_head_angle(req.angle_deg)
    return {"status": "ok" if success else "failed", "head_angle": req.angle_deg}


@app.post("/api/v1/robot/lift")
async def set_lift(req: LiftRequest):
    success = await local_vector_bridge.set_lift_height(req.height)
    return {"status": "ok" if success else "failed", "lift_height": req.height}


@app.post("/api/v1/robot/expression")
async def set_expression(req: ExpressionRequest):
    success = await local_vector_bridge.set_face_expression(req.expression)
    return {"status": "ok" if success else "failed", "expression": req.expression}


@app.post("/api/v1/robot/dock")
async def dock_robot():
    success = await local_vector_bridge.dock_on_charger()
    return {"status": "ok" if success else "failed"}


@app.post("/api/v1/robot/say")
async def say_text(req: SayRequest):
    success = await local_vector_bridge.say_text(req.text)
    return {"status": "ok" if success else "failed", "text": req.text}


@app.post("/api/v1/system/wake-pc")
async def wake_pc():
    success = local_wol_sentinel.send_wol_packet()
    return {"status": "sent" if success else "failed"}


@app.post("/api/v1/llm/chat")
async def chat_with_vector(req: ChatRequest):
    """Dynamic tiering chat endpoint (Gemini Live API or RTX 5070 Local LLM)."""
    response_text = llm_router.query_gemini(req.prompt)
    # Also trigger speech in Vector
    await local_vector_bridge.say_text(response_text)
    return {"response": response_text}


@app.post("/api/v1/agent/coding")
async def run_coding_task(req: CodingRequest):
    """Triggers Claude Code CLI in headless mode."""
    output = llm_router.execute_claude_code(req.task_prompt)
    return {"output": output}


def run():
    uvicorn.run(app, host=pc_config.host, port=pc_config.port)


if __name__ == "__main__":
    run()

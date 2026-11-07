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

from gateway.vector_bridge import VectorBridge
from gateway.wol_sentinel import WakeOnLanSentinel
from pc_agent.camera_ptz import Insta360Link2Controller, MockCamera
from pc_agent.config import pc_config
from pc_agent.llm_router import LLMRouter
from pc_agent.npu_engine import IntelNPUEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
logger = logging.getLogger("vector.pc_agent")

app = FastAPI(title="Vector PC Workstation Agent (RTX 5070 + NPU)", version="1.0.0")

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


# Models
class PTZRequest(BaseModel):
    pan_arcsec: int
    tilt_arcsec: int


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
    """Returns combined status of Workstation, Camera, NPU, and Vector."""
    robot_status = local_vector_bridge.get_status()
    npu_status = npu_engine.get_telemetry()
    return {
        "status": "ONLINE",
        "node": "PC Workstation (RTX 5070 + Intel NPU)",
        "robot": robot_status,
        "camera": {
            "mock": pc_config.mock_camera,
            "current_pan_arcsec": camera.current_pan,
            "current_tilt_arcsec": camera.current_tilt,
            "current_pan_deg": round(camera.current_pan / 3600.0, 1),
            "current_tilt_deg": round(camera.current_tilt / 3600.0, 1),
        },
        "npu": npu_status,
    }


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

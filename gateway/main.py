"""
Gateway Main Entrypoint for Arduino UNO Q.
Coordinates VectorBridge, WakeOnLanSentinel, AudioPipeline, MemoryManager, and IntentParser.
Exposes a lightweight REST API on port 8000 for local telemetry and remote triggers.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any, Dict

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
import uvicorn

from gateway.audio_pipeline import HalfDuplexAEC, pcm_to_wav, resample_pcm_24k_to_16k
from gateway.config import config
from gateway.intent_parser import OfflineIntentParser
from gateway.uno_q_bridge import UnoQBridge
from gateway.vector_bridge import VectorBridge
from memory.db import MemoryManager
from gateway.wol_sentinel import WakeOnLanSentinel

logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)
logger = logging.getLogger("vector.gateway")

app = FastAPI(title="Vector 2.0 Edge Gateway (Arduino UNO Q)", version="1.1.0")

# Service singletons
vector_bridge = VectorBridge(
    mock_mode=config.mock_robot,
    serial=config.vector_robot_serial,
    ip=config.vector_robot_ip,
)
wol_sentinel = WakeOnLanSentinel(
    pc_mac=config.pc_mac_address,
    pc_ip=config.pc_host,
    pc_port=config.pc_port,
    wol_port=config.pc_wol_port,
)
uno_q_bridge = UnoQBridge()
audio_aec = HalfDuplexAEC()
intent_parser = OfflineIntentParser()
memory_manager = MemoryManager(db_path=config.memory_db_path, vector_dim=config.vector_dim)


# Request Models
class CommandRequest(BaseModel):
    command: str


class LedStateRequest(BaseModel):
    state: str


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


class MemoryStoreRequest(BaseModel):
    fact: str
    embedding: list[float]
    category: str = "general"


@app.on_event("startup")
async def on_startup():
    logger.info("Initializing Gateway services on Arduino UNO Q...")
    await vector_bridge.initialize()
    uno_q_bridge.set_led_status("IDLE")
    await wol_sentinel.start_monitoring(poll_interval_sec=5.0)
    logger.info("Gateway services started successfully.")


@app.on_event("shutdown")
async def on_shutdown():
    wol_sentinel.stop_monitoring()
    logger.info("Gateway services shut down cleanly.")


@app.get("/")
async def root():
    return {
        "service": "Vector 2.0 Edge Gateway",
        "node": "Arduino UNO Q (4GB)",
        "mock_mode": config.mock_robot,
        "pc_awake": wol_sentinel.is_pc_awake,
        "uno_q_led_state": uno_q_bridge.current_state,
    }


@app.get("/telemetry")
async def get_telemetry():
    """Returns combined status of Vector, UNO Q MCU, PC sentinel, and memory."""
    robot_status = vector_bridge.get_status()
    return {
        "robot": robot_status,
        "uno_q": uno_q_bridge.get_status(),
        "sentinel": {
            "pc_host": config.pc_host,
            "pc_mac": config.pc_mac_address,
            "is_pc_awake": wol_sentinel.is_pc_awake,
        },
        "audio": {
            "is_mic_muted": audio_aec.is_mic_muted,
            "is_speaking": audio_aec.is_speaking,
        },
        "config": {
            "mock_robot": config.mock_robot,
            "mock_camera": config.mock_camera,
        },
    }


@app.post("/uno-q/led")
async def set_uno_q_led(req: LedStateRequest):
    """Sets the 8x13 Blue LED Matrix pattern on the Arduino UNO Q STM32U585 MCU."""
    return uno_q_bridge.set_led_status(req.state)


@app.post("/wake-pc")
async def trigger_wake_pc():
    """Fires Wake-on-LAN magic packet to wake the RTX 5070 workstation."""
    uno_q_bridge.set_led_status("WAKE_PC")
    success = wol_sentinel.send_wol_packet()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send WoL packet")
    return {"status": "sent", "pc_mac": config.pc_mac_address, "led_state": uno_q_bridge.current_state}


@app.post("/robot/say")
async def robot_say(req: SayRequest):
    """Speaks text through Vector's speaker with Half-Duplex AEC echo protection."""
    await audio_aec.notify_speech_started()
    try:
        success = await vector_bridge.say_text(req.text)
    finally:
        await audio_aec.notify_speech_finished()
    return {"status": "ok" if success else "failed", "text": req.text}


@app.post("/robot/drive")
async def robot_drive(req: DriveRequest):
    success = await vector_bridge.drive_straight(req.distance_mm, req.speed_mmps)
    return {"status": "ok" if success else "failed", "telemetry": vector_bridge.get_status()}


@app.post("/robot/turn")
async def robot_turn(req: TurnRequest):
    success = await vector_bridge.turn_in_place(req.angle_deg, req.speed_dps)
    return {"status": "ok" if success else "failed", "telemetry": vector_bridge.get_status()}


@app.post("/robot/head")
async def robot_head(req: HeadRequest):
    success = await vector_bridge.set_head_angle(req.angle_deg)
    return {"status": "ok" if success else "failed", "head_angle": req.angle_deg}


@app.post("/robot/lift")
async def robot_lift(req: LiftRequest):
    success = await vector_bridge.set_lift_height(req.height)
    return {"status": "ok" if success else "failed", "lift_height": req.height}


@app.post("/robot/dock")
async def robot_dock():
    success = await vector_bridge.dock_on_charger()
    return {"status": "ok" if success else "failed"}


@app.post("/offline/intent")
async def parse_and_execute_offline(req: CommandRequest):
    """Parses Turkish user command offline and triggers local action."""
    parsed = intent_parser.parse(req.command)
    logger.info(f"Parsed offline intent: {parsed.intent_type} (conf={parsed.confidence:.2f})")

    # Action dispatch
    if parsed.intent_type == "WAKE_PC":
        wol_sentinel.send_wol_packet()
    elif parsed.intent_type == "DOCK_ROBOT":
        await vector_bridge.dock_on_charger()
    elif parsed.intent_type == "HEAD_CONTROL":
        await vector_bridge.set_head_angle(parsed.parameters.get("angle", 0.0))

    # Respond with speech
    await audio_aec.notify_speech_started()
    try:
        await vector_bridge.say_text(parsed.speech_response)
    finally:
        await audio_aec.notify_speech_finished()

    return {
        "intent": parsed.intent_type,
        "confidence": parsed.confidence,
        "speech_response": parsed.speech_response,
        "parameters": parsed.parameters,
    }


@app.post("/memory/store")
async def store_memory_endpoint(req: MemoryStoreRequest):
    """Stores fact into sqlite-vec database."""
    try:
        mem_id = memory_manager.store_memory(
            fact=req.fact,
            embedding=req.embedding,
            category=req.category,
        )
        return {"status": "stored", "id": mem_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/memory/recent")
async def get_recent_memories(limit: int = 10, category: str = Query(None)):
    memories = memory_manager.get_recent_memories(limit=limit, category=category)
    return {"memories": memories}


def run():
    uvicorn.run(app, host=config.gateway_host, port=config.gateway_port)


if __name__ == "__main__":
    run()

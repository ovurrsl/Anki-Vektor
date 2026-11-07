"""
Integration tests for PC Agent FastAPI server and endpoints.
"""

from fastapi.testclient import TestClient
from pc_agent.server import app

client = TestClient(app)


def test_pc_agent_status():
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ONLINE"
    assert "robot" in data
    assert "camera" in data
    assert "npu" in data


def test_camera_snapshot():
    resp = client.get("/api/v1/camera/snapshot")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/jpeg"
    assert len(resp.content) > 100
    assert resp.content[:2] == b"\xff\xd8"


def test_camera_ptz():
    resp = client.post("/api/v1/camera/ptz", json={"pan_arcsec": 3600, "tilt_arcsec": -3600})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["pan_arcsec"] == 3600
    assert data["tilt_arcsec"] == -3600


def test_robot_drive_and_say():
    resp_drive = client.post("/api/v1/robot/drive", json={"distance_mm": 50.0, "speed_mmps": 50.0})
    assert resp_drive.status_code == 200
    assert resp_drive.json()["status"] == "ok"

    resp_say = client.post("/api/v1/robot/say", json={"text": "Dashboard test"})
    assert resp_say.status_code == 200
    assert resp_say.json()["status"] == "ok"


def test_dashboard_html():
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert "ANKI" in resp.text
    assert "VECTOR" in resp.text

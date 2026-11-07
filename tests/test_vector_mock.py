"""
Unit tests for MockVectorRobot and VectorBridge.
"""

import pytest
from gateway.vector_bridge import MockVectorRobot, VectorBridge


@pytest.mark.asyncio
async def test_mock_robot_drive_and_turn():
    robot = MockVectorRobot(serial="TEST_001")
    await robot.connect()
    assert robot.telemetry.connected is True

    # Initial position
    assert robot.telemetry.x == 0.0
    assert robot.telemetry.y == 0.0
    assert robot.telemetry.is_on_charger is True

    # Drive forward 100mm
    await robot.drive_straight(100.0, speed_mmps=50.0)
    assert robot.telemetry.x == 100.0
    assert robot.telemetry.is_on_charger is False

    # Turn in place 90 degrees
    await robot.turn_in_place(90.0, speed_dps=100.0)
    assert robot.telemetry.heading_deg == 90.0

    # Drive forward 50mm along Y axis
    await robot.drive_straight(50.0, speed_mmps=50.0)
    assert round(robot.telemetry.y, 1) == 50.0


@pytest.mark.asyncio
async def test_mock_robot_head_and_lift_limits():
    robot = MockVectorRobot(serial="TEST_002")

    # Safe head range: -22.0 to 45.0
    await robot.set_head_angle(60.0)
    assert robot.telemetry.head_angle_deg == 45.0

    await robot.set_head_angle(-35.0)
    assert robot.telemetry.head_angle_deg == -22.0

    # Lift range: 0.0 to 1.0
    await robot.set_lift_height(1.5)
    assert robot.telemetry.lift_height == 1.0

    await robot.set_lift_height(-0.2)
    assert robot.telemetry.lift_height == 0.0


@pytest.mark.asyncio
async def test_mock_robot_speech_and_screen():
    robot = MockVectorRobot(serial="TEST_003")

    await robot.say_text("Merhaba Vector!")
    assert robot.telemetry.last_spoken_text == "Merhaba Vector!"
    assert robot.telemetry.is_speaking is False

    await robot.set_face_expression("sarcastic")
    assert robot.telemetry.current_expression == "sarcastic"


@pytest.mark.asyncio
async def test_vector_bridge_mock_dispatch():
    bridge = VectorBridge(mock_mode=True, serial="BRIDGE_001")
    init_ok = await bridge.initialize()
    assert init_ok is True

    status = bridge.get_status()
    assert status["connected"] is True
    assert "battery_percentage" in status

    # Verify action dispatches
    say_ok = await bridge.say_text("Test bridge")
    assert say_ok is True

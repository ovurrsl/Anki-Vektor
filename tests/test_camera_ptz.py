"""
Unit tests for Insta360 Link 2 Camera & MockCamera.
"""

from pc_agent.camera_ptz import MockCamera, round_to_arcsec_step


def test_arcsecond_quantization():
    # Hardware requires multiples of 3600
    assert round_to_arcsec_step(3600) == 3600
    assert round_to_arcsec_step(3700) == 3600
    assert round_to_arcsec_step(5500) == 7200
    assert round_to_arcsec_step(-3500) == -3600


def test_mock_camera_bounds_and_deskview():
    cam = MockCamera()

    # Move beyond limits -> should clamp
    cam.set_ptz(pan_arcsec=600000, tilt_arcsec=-400000)
    assert cam.current_pan == 480000  # Clamped to +480000
    assert cam.current_tilt == -300000  # Clamped to -300000

    # Set DeskView (-80° = -288000 arcsec)
    cam.set_desk_view()
    assert cam.current_pan == 0
    assert cam.current_tilt == -288000


def test_mock_camera_frame_capture():
    cam = MockCamera()
    frame = cam.capture_frame(robot_x=50.0, robot_y=20.0)
    assert isinstance(frame, bytes)
    assert len(frame) > 100
    # Standard JPEG SOI (Start Of Image) marker: 0xFF, 0xD8
    assert frame[:2] == b"\xff\xd8"

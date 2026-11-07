"""
Unit tests for Gateway Sentinel, Intent Parser, and Audio Pipeline.
"""

import asyncio
import pytest
import numpy as np

from gateway.wol_sentinel import create_magic_packet, WakeOnLanSentinel
from gateway.intent_parser import OfflineIntentParser
from gateway.audio_pipeline import (
    HalfDuplexAEC,
    create_wav_header,
    resample_pcm_24k_to_16k,
    pcm_to_wav,
)


def test_magic_packet_generation():
    mac = "AA:BB:CC:11:22:33"
    packet = create_magic_packet(mac)
    assert len(packet) == 102
    assert packet[:6] == b"\xff" * 6
    # 16 repetitions of 6 bytes = 96 bytes
    expected_mac_bytes = bytes.fromhex("AABBCC112233")
    assert packet[6:12] == expected_mac_bytes
    assert packet[-6:] == expected_mac_bytes


def test_invalid_mac_packet_generation():
    with pytest.raises(ValueError):
        create_magic_packet("INVALID_MAC")


def test_offline_intent_parser():
    parser = OfflineIntentParser()

    intent_wol = parser.parse("lütfen bilgisayarı açar mısın")
    assert intent_wol.intent_type == "WAKE_PC"
    assert intent_wol.confidence > 0.9

    intent_time = parser.parse("şu an saat kaç")
    assert intent_time.intent_type == "GET_TIME"

    intent_battery = parser.parse("batarya durumu nasıl")
    assert intent_battery.intent_type == "BATTERY_STATUS"

    intent_dock = parser.parse("yuvana dön ve dinlen")
    assert intent_dock.intent_type == "DOCK_ROBOT"

    intent_head = parser.parse("masaya bak lütfen")
    assert intent_head.intent_type == "HEAD_CONTROL"


def test_wav_header_and_resampling():
    # Generate 1 second of 24kHz synthetic 440Hz sine wave (24000 samples = 48000 bytes)
    t = np.linspace(0, 1.0, 24000, endpoint=False)
    sine_24k = (np.sin(2 * np.pi * 440 * t) * 30000).astype(np.int16).tobytes()

    # Resample to 16kHz
    pcm_16k = resample_pcm_24k_to_16k(sine_24k)
    num_samples_16k = len(pcm_16k) // 2
    # Should be close to 16000 samples
    assert abs(num_samples_16k - 16000) <= 2

    # Wrap into WAV
    wav_bytes = pcm_to_wav(pcm_16k, sample_rate=16000)
    assert len(wav_bytes) == len(pcm_16k) + 44
    assert wav_bytes[:4] == b"RIFF"
    assert wav_bytes[8:12] == b"WAVE"


@pytest.mark.asyncio
async def test_half_duplex_aec():
    aec = HalfDuplexAEC(post_speech_tail_sec=0.1)
    assert aec.can_process_audio_input() is True

    # Speech starts -> mic must mute
    await aec.notify_speech_started()
    assert aec.is_speaking is True
    assert aec.is_mic_muted is True
    assert aec.can_process_audio_input() is False

    # Speech finishes -> mic remains muted during reverberation tail
    await aec.notify_speech_finished()
    assert aec.is_speaking is False
    assert aec.is_mic_muted is True  # still in tail

    # After tail delay -> mic unmuted
    await asyncio.sleep(0.15)
    assert aec.is_mic_muted is False
    assert aec.can_process_audio_input() is True

"""
Audio Pipeline Module.
Implements Half-Duplex Acoustic Echo Cancellation (AEC) and 24kHz -> 16kHz audio resampling.
Bridges Google Gemini Live API audio output to Vector 2.0's 16kHz mono speaker.
"""

from __future__ import annotations

import asyncio
import io
import logging
import struct
import time
from typing import Optional

import numpy as np

logger = logging.getLogger("vector.audio")

try:
    import soxr
    SOXR_AVAILABLE = True
except ImportError:
    SOXR_AVAILABLE = False
    logger.warning("soxr library not found. Falling back to numpy linear resampling.")


def create_wav_header(
    pcm_length_bytes: int,
    sample_rate: int = 16000,
    channels: int = 1,
    bits_per_sample: int = 16,
) -> bytes:
    """
    Constructs a standard 44-byte RIFF/WAV binary header for raw PCM audio.
    """
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)
    riff_chunk_size = 36 + pcm_length_bytes

    header = bytearray()
    # RIFF header
    header.extend(b"RIFF")
    header.extend(struct.pack("<I", riff_chunk_size))
    header.extend(b"WAVE")
    # fmt sub-chunk
    header.extend(b"fmt ")
    header.extend(struct.pack("<I", 16))          # Subchunk1Size (16 for PCM)
    header.extend(struct.pack("<H", 1))           # AudioFormat (1 for PCM)
    header.extend(struct.pack("<H", channels))     # NumChannels
    header.extend(struct.pack("<I", sample_rate))  # SampleRate
    header.extend(struct.pack("<I", byte_rate))   # ByteRate
    header.extend(struct.pack("<H", block_align))  # BlockAlign
    header.extend(struct.pack("<H", bits_per_sample))  # BitsPerSample
    # data sub-chunk
    header.extend(b"data")
    header.extend(struct.pack("<I", pcm_length_bytes))
    return bytes(header)


def resample_pcm_24k_to_16k(pcm_bytes_24k: bytes) -> bytes:
    """
    Downsamples 24,000 Hz 16-bit mono PCM bytes to 16,000 Hz 16-bit mono PCM.
    Gemini Live API outputs 24kHz; Vector speaker accepts up to 16,025 Hz.
    """
    if not pcm_bytes_24k:
        return b""

    # Convert raw bytes to int16 numpy array
    audio_in = np.frombuffer(pcm_bytes_24k, dtype=np.int16)

    if SOXR_AVAILABLE:
        # High quality polyphase resampling via libsoxr
        audio_out = soxr.resample(audio_in, in_rate=24000, out_rate=16000, quality="HQ")
        return audio_out.astype(np.int16).tobytes()

    # Fallback linear interpolation
    num_input_samples = len(audio_in)
    num_output_samples = int(num_input_samples * 16000 / 24000)
    indices = np.linspace(0, num_input_samples - 1, num_output_samples)
    audio_out = np.interp(indices, np.arange(num_input_samples), audio_in).astype(np.int16)
    return audio_out.tobytes()


def pcm_to_wav(pcm_bytes: bytes, sample_rate: int = 16000) -> bytes:
    """Wraps raw PCM bytes with a valid WAV header."""
    header = create_wav_header(len(pcm_bytes), sample_rate=sample_rate)
    return header + pcm_bytes


class HalfDuplexAEC:
    """
    Half-Duplex Acoustic Echo Cancellation state controller.
    Prevents acoustic feedback loop by muting microphone listening
    while Vector is speaking, plus a reverberation tail delay.
    """

    def __init__(self, post_speech_tail_sec: float = 0.4):
        self.post_speech_tail_sec = post_speech_tail_sec
        self.is_speaking = False
        self.is_mic_muted = False
        self._lock = asyncio.Lock()
        self._tail_task: Optional[asyncio.Task] = None

    async def notify_speech_started(self) -> None:
        """Called when robot starts playing sound/speech."""
        async with self._lock:
            if self._tail_task and not self._tail_task.done():
                self._tail_task.cancel()
            self.is_speaking = True
            self.is_mic_muted = True
            logger.debug("[AEC] Speech STARTED -> Microphone MUTED")

    async def notify_speech_finished(self) -> None:
        """Called when robot stops playing sound. Starts reverberation tail timer."""
        async with self._lock:
            self.is_speaking = False

            async def _tail_delay():
                logger.debug(f"[AEC] Waiting {self.post_speech_tail_sec}s tail decay...")
                await asyncio.sleep(self.post_speech_tail_sec)
                self.is_mic_muted = False
                logger.debug("[AEC] Reverberation tail passed -> Microphone UNMUTED")

            self._tail_task = asyncio.create_task(_tail_delay())

    def can_process_audio_input(self) -> bool:
        """Returns True if microphone input is safe to pass to wake word/STT."""
        return not self.is_mic_muted

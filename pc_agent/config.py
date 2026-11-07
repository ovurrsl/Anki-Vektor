"""
PC Agent Configuration Module.
Parameters for the RTX 5070 + Intel NPU workstation services and dashboard.
"""

import os
from dataclasses import dataclass, field


@dataclass
class PCAgentConfig:
    host: str = field(default_factory=lambda: os.getenv("PC_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PC_PORT", "8080")))
    agent_token: str = field(
        default_factory=lambda: os.getenv("PC_AGENT_TOKEN", "secret-token")
    )
    mock_camera: bool = field(
        default_factory=lambda: os.getenv("MOCK_CAMERA", "True").lower() in ("true", "1", "yes")
    )
    camera_device_index: int = field(
        default_factory=lambda: int(os.getenv("CAMERA_DEVICE_INDEX", "0"))
    )

    # Local LLM on RTX 5070 (12GB VRAM)
    local_llm_url: str = field(
        default_factory=lambda: os.getenv("LOCAL_LLM_URL", "http://127.0.0.1:8001/v1")
    )
    local_llm_model: str = field(
        default_factory=lambda: os.getenv("LOCAL_LLM_MODEL", "Qwen2.5-14B-Instruct-Q4_K_M")
    )

    # Google Gemini API
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    )

    # Gateway address (Arduino UNO Q)
    gateway_url: str = field(
        default_factory=lambda: os.getenv("GATEWAY_URL", "http://127.0.0.1:8000")
    )


pc_config = PCAgentConfig()

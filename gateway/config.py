"""
Gateway Configuration Module.
Loads environment variables and sets operational parameters for Arduino UNO Q Gateway.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GatewayConfig:
    # Mode flags
    mock_robot: bool = field(
        default_factory=lambda: os.getenv("MOCK_ROBOT", "True").lower() in ("true", "1", "yes")
    )
    mock_camera: bool = field(
        default_factory=lambda: os.getenv("MOCK_CAMERA", "True").lower() in ("true", "1", "yes")
    )
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Gateway server settings
    gateway_host: str = field(default_factory=lambda: os.getenv("GATEWAY_HOST", "0.0.0.0"))
    gateway_port: int = field(default_factory=lambda: int(os.getenv("GATEWAY_PORT", "8000")))
    gateway_token: str = field(
        default_factory=lambda: os.getenv("GATEWAY_AUTH_TOKEN", "secret-token")
    )

    # PC Workstation (RTX 5070 + NPU) settings
    pc_host: str = field(default_factory=lambda: os.getenv("PC_HOST", "127.0.0.1"))
    pc_port: int = field(default_factory=lambda: int(os.getenv("PC_PORT", "8080")))
    pc_mac_address: str = field(
        default_factory=lambda: os.getenv("PC_MAC_ADDRESS", "AA:BB:CC:DD:EE:FF")
    )
    pc_wol_port: int = field(default_factory=lambda: int(os.getenv("PC_WOL_PORT", "9")))
    pc_agent_token: str = field(
        default_factory=lambda: os.getenv("PC_AGENT_TOKEN", "secret-token")
    )

    # Vector 2.0 Robot settings
    vector_robot_name: str = field(
        default_factory=lambda: os.getenv("VECTOR_ROBOT_NAME", "Vector-MOCK")
    )
    vector_robot_ip: str = field(
        default_factory=lambda: os.getenv("VECTOR_ROBOT_IP", "127.0.0.1")
    )
    vector_robot_serial: str = field(
        default_factory=lambda: os.getenv("VECTOR_ROBOT_SERIAL", "00000000")
    )
    vector_cert_path: str = field(
        default_factory=lambda: os.getenv("VECTOR_CERT_PATH", "")
    )

    # Memory Database settings
    memory_db_path: str = field(
        default_factory=lambda: os.getenv("MEMORY_DB_PATH", "vector_memory.db")
    )
    vector_dim: int = field(
        default_factory=lambda: int(os.getenv("MEMORY_VECTOR_DIMENSION", "768"))
    )

    # Cloud AI
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    )


# Singleton instance
config = GatewayConfig()

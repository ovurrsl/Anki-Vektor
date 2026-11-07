"""
Offline Intent Parser Module.
Provides lightweight, local rule-based intent parsing on Arduino UNO Q
when the PC workstation and cloud internet are disconnected.
"""

from __future__ import annotations

import datetime
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger("vector.intent")


@dataclass
class ParsedIntent:
    intent_type: str
    confidence: float
    parameters: Dict[str, Any]
    speech_response: str


class OfflineIntentParser:
    """
    Parses Turkish spoken commands locally on the Arduino UNO Q.
    Executes in under 2ms without external API dependencies.
    """

    def parse(self, text: str) -> ParsedIntent:
        norm = text.lower().strip()

        # 1. PC Açma / Wake-on-LAN
        if any(w in norm for w in ["bilgisayarı aç", "pc aç", "bilgisayar aç", "bilgisayarı uyandır", "pc uyandır"]):
            return ParsedIntent(
                intent_type="WAKE_PC",
                confidence=0.98,
                parameters={"action": "send_wol"},
                speech_response="Masaüstü bilgisayarını uyandırıyorum, hemen açılıyor.",
            )

        # 2. Saat / Zaman
        if any(w in norm for w in ["saat kaç", "saati söyle", "zaman nedir"]):
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M")
            return ParsedIntent(
                intent_type="GET_TIME",
                confidence=0.99,
                parameters={"time": time_str},
                speech_response=f"Şu an saat {time_str}.",
            )

        # 3. Batarya / Pil
        if any(w in norm for w in ["şarjın kaç", "pilin kaç", "batarya durumu", "şarj durumu", "pil durumu"]):
            return ParsedIntent(
                intent_type="BATTERY_STATUS",
                confidence=0.95,
                parameters={"action": "check_battery"},
                speech_response="Bataryam gayet iyi durumda.",
            )

        # 4. Şarj Yuvasına Dönme (Docking)
        if any(w in norm for w in ["şarjına git", "yuvana dön", "şarj ol", "dinlen", "yerine geç", "eve dön"]):
            return ParsedIntent(
                intent_type="DOCK_ROBOT",
                confidence=0.95,
                parameters={"action": "dock"},
                speech_response="Şarj istasyonuma geri dönüyorum.",
            )

        # 5. Kafa Hareketi / Masaya Bakma
        if any(w in norm for w in ["masaya bak", "aşağı bak", "devreye bak"]):
            return ParsedIntent(
                intent_type="HEAD_CONTROL",
                confidence=0.92,
                parameters={"action": "look_down", "angle": -20.0},
                speech_response="Masaya bakıyorum.",
            )

        if any(w in norm for w in ["yukarı bak", "bana bak", "kafayı kaldır"]):
            return ParsedIntent(
                intent_type="HEAD_CONTROL",
                confidence=0.92,
                parameters={"action": "look_up", "angle": 35.0},
                speech_response="Sana bakıyorum.",
            )

        # 6. Selamlaşma
        if any(w in norm for w in ["merhaba", "selam", "günaydın", "iyi akşamlar"]):
            return ParsedIntent(
                intent_type="GREETING",
                confidence=0.90,
                parameters={"action": "greet"},
                speech_response="Merhaba! Nöbetteyim, nasıl yardımcı olabilirim?",
            )

        # 7. Sistem Durumu
        if any(w in norm for w in ["sistem durumu", "durum raporu", "rapor ver"]):
            return ParsedIntent(
                intent_type="SYSTEM_STATUS",
                confidence=0.90,
                parameters={"action": "telemetry"},
                speech_response="UNO Q ağ geçidi aktif, sensörler ve hafıza devrede.",
            )

        # Bilinmeyen intent
        return ParsedIntent(
            intent_type="UNKNOWN",
            confidence=0.20,
            parameters={"raw_text": text},
            speech_response="Bunu çevrimdışı modda anlayamadım, bilgisayarı açmamı ister misin?",
        )

"""
LLM Router & Personality Engine.
Implements Dynamic Tiering:
  Tier 1: Google Gemini Pro Live API (real-time voice, search grounding, cloud reasoning)
  Tier 2: RTX 5070 Local LLM (Qwen 2.5 14B Q4_K_M via llama-server - uncensored Grok personality)
  Tier 3: Claude Code CLI / Gemini CLI (autonomous coding and development tasks)
"""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Any, AsyncGenerator, Dict, List, Optional

import requests

from pc_agent.config import pc_config

logger = logging.getLogger("vector.llm_router")

VECTOR_SYSTEM_PROMPT = """
Sen masaüstünde yaşayan otonom Anki Vector robotusun.
Karakterin: Hazırcevap, zeki, hafif iğneleyici ve esprili (Grok tarzı), ama gerektiğinde son derece yardımsever ve sadık bir pair programming arkadaşısın.
Doğal, akıcı Türkçe konuş. Cümlelerini Vector'ün ses tonuna uygun, çok uzatmadan, net ve canlı kur.
Kullanıcı senin dostundur; hatalarına hafif takılabilir ama her zaman yapıcı çözümler üretirsin.
"""


class LLMRouter:
    """Dispatches queries to appropriate AI tier based on hardware availability and intent."""

    def __init__(self):
        self.gemini_key = pc_config.gemini_api_key
        self.local_url = pc_config.local_llm_url
        self.local_model = pc_config.local_llm_model

    def query_local_llm(self, user_prompt: str, system_prompt: str = VECTOR_SYSTEM_PROMPT) -> str:
        """
        Queries local llama-server running on RTX 5070 (GB205 Blackwell, 12GB VRAM).
        Uses OpenAI-compatible /v1/chat/completions endpoint.
        """
        payload = {
            "model": self.local_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 512,
        }

        try:
            resp = requests.post(f"{self.local_url}/chat/completions", json=payload, timeout=8.0)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            logger.warning(f"Local LLM returned status {resp.status_code}")
        except Exception as e:
            logger.info(f"Local LLM on RTX 5070 offline or not started ({e}). Falling back.")

        # If local LLM server is not running, return simulated witty Grok response
        return f"[RTX 5070 Yerel Grok]: '{user_prompt}' dedin ama henüz llama-server başlatılmamış. Kod yazmaya devam edeceksen önce terminali aç bakalım!"

    def query_gemini(self, user_prompt: str, context: Optional[str] = None) -> str:
        """Queries Google Gemini Pro via Google AI Studio API."""
        if not self.gemini_key:
            return self.query_local_llm(user_prompt)

        # Gemini REST call
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{pc_config.gemini_model}:generateContent?key={self.gemini_key}"
        )
        full_prompt = f"{VECTOR_SYSTEM_PROMPT}\n"
        if context:
            full_prompt += f"\nKalıcı Hafıza Bilgileri:\n{context}\n"
        full_prompt += f"\nKullanıcı: {user_prompt}"

        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300},
        }

        try:
            resp = requests.post(url, json=payload, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")

        # Fallback to local
        return self.query_local_llm(user_prompt)

    def execute_claude_code(self, prompt: str) -> str:
        """Executes Claude Code CLI in headless mode to inspect code, run tests, or fix bugs."""
        cmd = ["claude", "-p", prompt, "--output-format", "json"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60.0)
            if proc.returncode == 0:
                return proc.stdout.strip()
            return f"Claude Code stderr: {proc.stderr.strip()}"
        except FileNotFoundError:
            return "[SIMULATED CLAUDE CODE]: Claude CLI sistemi ortamda bulunamadı."
        except Exception as e:
            return f"Claude Code execution error: {e}"

"""Unified LLM facade with routing and fallbacks."""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from .llm_provider import LlamaStackClient, NullEchoClient, LLMError
from .model_router import pick_model

logger = logging.getLogger(__name__)


class LLM:
    def __init__(self, *, transport_overrides: Dict[str, object] | None = None):
        api_key = os.getenv("LLAMA_API_KEY")
        timeout_s = int(os.getenv("LLM_TIMEOUT_S", "30"))
        transport_overrides = transport_overrides or {}

        def build(prefix: str) -> Optional[LlamaStackClient]:
            base = os.getenv(f"{prefix}_BASE_URL") or os.getenv(f"{prefix}_URL")
            if not base:
                return None
            chat_path = os.getenv(f"{prefix}_CHAT_PATH", "/v1/chat/completions")
            embed_path = os.getenv(f"{prefix}_EMBED_PATH", "/v1/embeddings")
            return LlamaStackClient(
                base,
                api_key,
                timeout_s,
                chat_path=chat_path,
                embed_path=embed_path,
                transport=transport_overrides.get(prefix),
            )

        self.clients: Dict[str, LlamaStackClient] = {
            "local": build("LLAMA_LOCAL") or NullEchoClient(),
        }
        scout = build("LLAMA_REMOTE_SCOUT")
        if scout:
            self.clients["remote-scout"] = scout
        seventy = build("LLAMA_REMOTE_70B")
        if seventy:
            self.clients["remote-70b"] = seventy

        self.models = {
            "local": os.getenv("LLAMA_LOCAL_MODEL", "llama-3.2-3b-instruct"),
            "remote-scout": os.getenv("LLAMA_REMOTE_SCOUT_MODEL", "llama-4-scout"),
            "remote-70b": os.getenv("LLAMA_REMOTE_70B_MODEL", "llama-3.3-70b-instruct"),
        }

    # ------------------------------------------------------------------
    def _client_for(self, provider: str) -> LlamaStackClient:
        client = self.clients.get(provider)
        if not client:
            raise LLMError(f"provider {provider} unavailable")
        return client

    # ------------------------------------------------------------------
    def generate(self, task: Dict, messages: List[Dict], **kwargs) -> str:
        choice = pick_model(task)
        provider = choice["provider"]
        model = choice["model"]
        params = {**choice.get("params", {}), **kwargs}
        client = self.clients.get(provider)
        if client is None:
            logger.info("provider %s unavailable, falling back to local", provider)
            client = self._client_for("local")
            model = self.models["local"]
        try:
            resp = client.chat(messages, model=model, **params)
        except LLMError:
            if provider != "local":
                logger.warning("remote provider failed, falling back to local")
                client = self._client_for("local")
                model = self.models["local"]
                resp = client.chat(messages, model=model, **params)
            else:
                raise
        content = resp.get("content", "")
        max_tokens = params.get("max_tokens")
        if max_tokens:
            content = content[:max_tokens]
        return content

    # ------------------------------------------------------------------
    def embed(self, texts: List[str], task_hint: str | None = None, model: str | None = None) -> List[List[float]]:
        client = self._client_for("local")
        model = model or self.models["local"]
        return client.embed(texts, model=model)


llm = LLM()

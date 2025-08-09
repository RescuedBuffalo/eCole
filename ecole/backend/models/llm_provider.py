import json
import logging
from typing import List, Dict, Optional

import httpx
from pydantic import BaseModel, ValidationError
from tenacity import Retrying, stop_after_attempt, wait_exponential_jitter


logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when the LLM provider fails."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class LLMProvider:
    """Abstract interface for LLM interactions."""

    def chat(self, messages: List[Dict], model: Optional[str] = None, **kwargs) -> Dict:
        raise NotImplementedError

    def embed(self, texts: List[str], model: Optional[str] = None, **kwargs) -> List[List[float]]:
        raise NotImplementedError


class _ChatChoice(BaseModel):
    message: Dict[str, str]


class _ChatResponse(BaseModel):
    choices: List[_ChatChoice]


class _EmbeddingData(BaseModel):
    embedding: List[float]


class _EmbeddingResponse(BaseModel):
    data: List[_EmbeddingData]


class LlamaStackClient(LLMProvider):
    """Client for Llama Stack or OpenAI compatible APIs."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout_s: int = 30,
        chat_path: str = "/v1/chat/completions",
        embed_path: str = "/v1/embeddings",
        transport: httpx.BaseTransport | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.chat_path = chat_path
        self.embed_path = embed_path
        self._client = httpx.Client(transport=transport)

    # ------------------------------------------------------------------
    def _make_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(self, path: str, payload: Dict) -> httpx.Response:
        for attempt in Retrying(
            stop=stop_after_attempt(3),
            wait=wait_exponential_jitter(initial=1, max=8),
            reraise=True,
        ):
            with attempt:
                resp = self._client.post(
                    f"{self.base_url}{path}",
                    json=payload,
                    headers=self._make_headers(),
                    timeout=self.timeout_s,
                )
                resp.raise_for_status()
                return resp

    # ------------------------------------------------------------------
    def chat(self, messages: List[Dict], model: Optional[str] = None, **kwargs) -> Dict:
        payload = {"model": model, "messages": messages}
        payload.update(kwargs)
        try:
            resp = self._request(self.chat_path, payload)
            data = resp.json()
            parsed = _ChatResponse(**data)
            content = parsed.choices[0].message.get("content", "")
            return {"content": content, "raw": data}
        except (httpx.HTTPError, ValidationError, KeyError, IndexError) as e:
            logger.warning("chat request failed: %s", e)
            raise LLMError(str(e))

    def embed(self, texts: List[str], model: Optional[str] = None, **kwargs) -> List[List[float]]:
        payload = {"model": model, "input": texts}
        payload.update(kwargs)
        try:
            resp = self._request(self.embed_path, payload)
            data = resp.json()
            parsed = _EmbeddingResponse(**data)
            return [d.embedding for d in parsed.data]
        except (httpx.HTTPError, ValidationError, KeyError, IndexError) as e:
            logger.warning("embedding request failed: %s", e)
            raise LLMError(str(e))


class NullEchoClient(LLMProvider):
    """Simple echo client for development and tests."""

    def chat(self, messages: List[Dict], model: Optional[str] = None, **kwargs) -> Dict:
        last = messages[-1]["content"] if messages else ""
        return {"content": f"echo: {last}"}

    def embed(self, texts: List[str], model: Optional[str] = None, **kwargs) -> List[List[float]]:
        return [[float(len(t))] for t in texts]

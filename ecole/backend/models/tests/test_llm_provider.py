import httpx
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from ecole.backend.models.llm_provider import LlamaStackClient, LLMError


def make_client(handler):
    transport = httpx.MockTransport(handler)
    return LlamaStackClient("https://example.com", api_key=None, timeout_s=1, transport=transport)


def test_chat_success():
    def handler(request):
        return httpx.Response(200, json={"choices": [{"message": {"content": "hi"}}]})

    client = make_client(handler)
    resp = client.chat([{"role": "user", "content": "hi"}], model="m")
    assert resp["content"] == "hi"


def test_chat_retry(monkeypatch):
    attempts = {"n": 0}

    def handler(request):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise httpx.ReadTimeout("timeout")
        return httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})

    client = make_client(handler)
    resp = client.chat([{"role": "user", "content": "hi"}], model="m")
    assert resp["content"] == "ok"
    assert attempts["n"] == 3


def test_chat_http_error():
    def handler(request):
        return httpx.Response(500, json={"error": "boom"})

    client = make_client(handler)
    with pytest.raises(LLMError):
        client.chat([{"role": "user", "content": "hi"}], model="m")

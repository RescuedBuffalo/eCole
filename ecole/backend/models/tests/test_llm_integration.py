import json
import sys
import os

import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from ecole.backend.models.llm import LLM


def test_generate_fallback_and_trim(monkeypatch):
    # setup env
    monkeypatch.setenv("LLAMA_LOCAL_BASE_URL", "https://local")
    monkeypatch.setenv("LLAMA_LOCAL_MODEL", "local")
    monkeypatch.setenv("LLAMA_REMOTE_70B_URL", "https://remote")
    monkeypatch.setenv("LLAMA_REMOTE_70B_MODEL", "r70b")

    def remote_handler(request: httpx.Request):
        return httpx.Response(500, json={"error": "boom"})

    captured = {}

    def local_handler(request: httpx.Request):
        captured["json"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"choices": [{"message": {"content": "abcdefghij"}}]})

    transports = {
        "LLAMA_REMOTE_70B": httpx.MockTransport(remote_handler),
        "LLAMA_LOCAL": httpx.MockTransport(local_handler),
    }
    model = LLM(transport_overrides=transports)

    messages = [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "hello"},
    ]
    task = {
        "type": "complex_reasoning",
        "expected_context_tokens": 10,
        "expected_output_tokens": 10,
    }

    reply = model.generate(task, messages, max_tokens=5)
    assert reply == "abcde"
    assert captured["json"]["messages"] == messages

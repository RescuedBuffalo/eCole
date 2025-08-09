import os
import sys
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

import ecole.backend.models.model_router as model_router


def get_router(monkeypatch):
    monkeypatch.setenv("LLAMA_LOCAL_MODEL", "local")
    monkeypatch.setenv("LLAMA_REMOTE_SCOUT_MODEL", "scout")
    monkeypatch.setenv("LLAMA_REMOTE_70B_MODEL", "70b")
    monkeypatch.setenv("LLAMA_REMOTE_SCOUT_URL", "https://scout")
    monkeypatch.setenv("LLAMA_REMOTE_70B_URL", "https://70b")
    importlib.reload(model_router)
    return model_router


def test_default_local(monkeypatch):
    mr = get_router(monkeypatch)
    monkeypatch.delenv("ECOLE_FORCE_PROVIDER", raising=False)
    res = mr.pick_model({"type": "general", "expected_context_tokens": 10, "expected_output_tokens": 10})
    assert res["provider"] == "local"
    assert res["model"] == "local"


def test_scout_by_context(monkeypatch):
    mr = get_router(monkeypatch)
    res = mr.pick_model({"type": "general", "expected_context_tokens": 150_000, "expected_output_tokens": 10})
    assert res["provider"] == "remote-scout"
    assert res["model"] == "scout"


def test_scout_by_type(monkeypatch):
    mr = get_router(monkeypatch)
    res = mr.pick_model({"type": "lifelog_long_context", "expected_context_tokens": 10, "expected_output_tokens": 10})
    assert res["provider"] == "remote-scout"


def test_70b_by_reasoning(monkeypatch):
    mr = get_router(monkeypatch)
    res = mr.pick_model({"type": "complex_reasoning", "expected_context_tokens": 10, "expected_output_tokens": 10})
    assert res["provider"] == "remote-70b"


def test_70b_by_output(monkeypatch):
    mr = get_router(monkeypatch)
    res = mr.pick_model({"type": "general", "expected_context_tokens": 10, "expected_output_tokens": 5000})
    assert res["provider"] == "remote-70b"


def test_force_override(monkeypatch):
    mr = get_router(monkeypatch)
    monkeypatch.setenv("ECOLE_FORCE_PROVIDER", "remote-70b")
    res = mr.pick_model({"type": "general", "expected_context_tokens": 10, "expected_output_tokens": 10})
    assert res["provider"] == "remote-70b"

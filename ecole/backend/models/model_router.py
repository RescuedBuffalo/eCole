"""Policy based model router."""
import os
from typing import Dict


LOCAL_MODEL = os.getenv("LLAMA_LOCAL_MODEL", "llama-3.2-3b-instruct")
SCOUT_MODEL = os.getenv("LLAMA_REMOTE_SCOUT_MODEL", "llama-4-scout")
MODEL_70B = os.getenv("LLAMA_REMOTE_70B_MODEL", "llama-3.3-70b-instruct")

SCOUT_AVAILABLE = os.getenv("LLAMA_REMOTE_SCOUT_BASE_URL") or os.getenv("LLAMA_REMOTE_SCOUT_URL")
MODEL_70B_AVAILABLE = os.getenv("LLAMA_REMOTE_70B_BASE_URL") or os.getenv("LLAMA_REMOTE_70B_URL")

MODEL_MAP = {
    "local": LOCAL_MODEL,
    "remote-scout": SCOUT_MODEL,
    "remote-70b": MODEL_70B,
}


def pick_model(task: Dict) -> Dict:
    """Pick a model based on task metadata."""
    force = os.getenv("ECOLE_FORCE_PROVIDER")
    if force in MODEL_MAP:
        provider = force
    else:
        if (
            SCOUT_AVAILABLE
            and (
                task.get("type") == "lifelog_long_context"
                or task.get("expected_context_tokens", 0) > 100_000
            )
        ):
            provider = "remote-scout"
        elif (
            MODEL_70B_AVAILABLE
            and (
                task.get("type") in {"complex_reasoning", "long_plan"}
                or task.get("expected_output_tokens", 0) > 2_000
            )
        ):
            provider = "remote-70b"
        else:
            provider = "local"
    model = MODEL_MAP.get(provider, LOCAL_MODEL)
    return {"provider": provider, "model": model, "params": {}}

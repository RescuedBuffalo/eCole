"""Tiny console demonstration for permission checks."""

from __future__ import annotations

from ..core.interfaces import ActionRequest
from ..permissions.action_registry import ActionRegistry


def main() -> None:
    """Run a simple permission demo."""

    registry = ActionRegistry.from_yaml()

    allowed_req = ActionRequest(
        run_id="demo",
        actor="executive",
        action_id="emit_response",
        payload={"text": "hi"},
    )
    registry.validate_payload(allowed_req.action_id, allowed_req.payload)
    allowed, reason = registry.is_allowed(allowed_req.actor, allowed_req.action_id)
    if allowed:
        print("\u2705 Allowed: emit_response")
    else:
        print(f"\u274c Denied: emit_response — {reason}")

    denied_req = ActionRequest(
        run_id="demo",
        actor="frontal",
        action_id="memory.save",
        payload={"kind": "event", "content": "test", "source": "user", "tags": []},
    )
    registry.validate_payload(denied_req.action_id, denied_req.payload)
    allowed, reason = registry.is_allowed(denied_req.actor, denied_req.action_id)
    if allowed:
        print("\u2705 Allowed: memory.save")
    else:
        print(f"\u274c Denied: memory.save — {reason}")


if __name__ == "__main__":
    main()

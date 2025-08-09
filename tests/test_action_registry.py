import pytest

from ecole.permissions.action_registry import ActionRegistry


def test_action_registry_loading_and_validation() -> None:
    registry = ActionRegistry.from_yaml()
    assert set(registry.all_actions()) == {
        "emit_response",
        "memory.save",
        "memory.query",
        "checklist.create",
        "checklist.update",
        "telemetry.log_event",
    }
    registry.validate_payload("emit_response", {"text": "hi"})
    with pytest.raises(ValueError):
        registry.validate_payload("emit_response", {"text": 123})

    registry.validate_payload(
        "memory.query",
        {"query": "q", "kind": "any", "k": 3},
    )
    with pytest.raises(ValueError):
        registry.validate_payload("memory.query", {"query": "q", "kind": "any", "k": 0})

from ecole.permissions.action_registry import ActionRegistry


def test_centralized_policy() -> None:
    registry = ActionRegistry.from_yaml()
    for action in registry.all_actions():
        allowed, reason = registry.is_allowed("executive", action)
        assert allowed, reason
    allowed, _ = registry.is_allowed("frontal", "memory.save")
    assert not allowed


def test_owner_allow_policy() -> None:
    registry = ActionRegistry.from_yaml()
    registry.execution_policy = "owner_allow"
    allowed, reason = registry.is_allowed("frontal", "checklist.create")
    assert allowed, reason
    allowed, _ = registry.is_allowed("frontal", "memory.save")
    assert not allowed

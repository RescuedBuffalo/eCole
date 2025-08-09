from ecole.core.interfaces import Decision, ModuleProposal, now_utc


def test_module_proposal_and_decision() -> None:
    proposal: ModuleProposal = {
        "module_id": "frontal",
        "action_id": "emit_response",
        "payload": {"text": "hi"},
        "utility_est": 0.5,
        "cost_est": 0.1,
        "confidence": 0.9,
        "rationale_log": "test",
    }
    decision = Decision(
        run_id="run1",
        proposals=[proposal],
        selected_index=0,
        reason="test",
        ts=now_utc(),
    )
    assert 0 <= proposal["utility_est"] <= 1
    assert 0 <= proposal["confidence"] <= 1
    assert decision.proposals[0]["module_id"] == "frontal"

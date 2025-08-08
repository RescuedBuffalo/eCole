from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    return [
        {
            "name": "suggest_habit",
            "content": "Maybe take a short walk?",
            "priority": "plan",
        }
    ]

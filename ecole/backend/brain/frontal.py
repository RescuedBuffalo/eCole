from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    if "?" in state.last_message:
        return [
            {
                "name": "ask_clarifying",
                "content": "Could you clarify your question?",
                "priority": "clarify",
            }
        ]
    return [
        {
            "name": "say",
            "content": "I hear you.",
            "priority": "comfort",
        }
    ]

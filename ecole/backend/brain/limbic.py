from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    return [
        {
            "name": "send_encouragement",
            "content": "You're doing great!",
            "priority": "comfort",
        }
    ]

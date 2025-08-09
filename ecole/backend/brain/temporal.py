from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    return [
        {
            "name": "write_memory",
            "content": state.last_message,
            "priority": "routine",
        }
    ]

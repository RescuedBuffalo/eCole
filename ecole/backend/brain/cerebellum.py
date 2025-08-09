from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    return [
        {
            "name": "start_routine",
            "content": "Initiating routine...",
            "priority": "routine",
        }
    ]

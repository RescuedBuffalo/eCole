from ..state.schema import AgentState


def propose(state: AgentState) -> list:
    return [
        {
            "name": "build_task_graph",
            "content": "Let's break it down step by step.",
            "priority": "plan",
        }
    ]

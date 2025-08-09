"""Registry of available actions and their required permissions.

This module replaces the previous YAML based configuration and provides
a Python native mapping that can be imported directly by other modules.
Each action is associated with a list of permission flags that must be
enabled on the ``AgentState.permissions`` object for the action to be
considered executable.
"""

# Mapping of action name to list of required permission attributes
ACTION_REGISTRY = {
    "say": ["speak"],
    "ask_clarifying": ["speak"],
    "propose_microplan": ["plan"],
    "set_local_reminder": ["memory_write"],
    "write_memory": ["memory_write"],
    "tag_core_memory": ["memory_write"],
    "recall_context": ["memory_read"],
    "summarize_day": ["memory_read"],
    "set_tone": ["speak"],
    "send_encouragement": ["speak"],
    "ask_mood_checkin": ["speak"],
    "suggest_break": ["speak"],
    "suggest_habit": ["plan"],
    "schedule_checkin": ["plan"],
    "reinforce_streak": ["plan"],
    "build_task_graph": ["plan"],
    "explain_step_by_step": ["plan"],
    "checklist_from_plan": ["plan"],
    "start_routine": ["routine"],
    "advance_routine": ["routine"],
    "stop_routine": ["routine"],
}


def required_permissions(action_name: str) -> list:
    """Return the list of required permissions for ``action_name``.

    Parameters
    ----------
    action_name:
        Name of the action whose permissions are requested.

    Returns
    -------
    list
        A list of permission attribute names.  If the action is unknown,
        an empty list is returned.
    """

    return ACTION_REGISTRY.get(action_name, [])


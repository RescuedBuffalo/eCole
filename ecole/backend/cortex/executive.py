from ..state.schema import AgentState
from ..models.llm import llm
from ..brain import frontal, temporal, limbic, basal_ganglia, parietal, cerebellum
from ..memory import store
from .action_registry import ACTION_REGISTRY

PRIORITY_ORDER = {"comfort": 0, "clarify": 1, "plan": 2, "routine": 3}


class ExecutiveController:
    def __init__(self, registry=None):
        self.registry = registry or ACTION_REGISTRY
        self.llm = llm
        self.modules = [frontal, temporal, limbic, basal_ganglia, parietal, cerebellum]

    def decide(self, state: AgentState) -> list:
        proposals = []
        for module in self.modules:
            proposals.extend(module.propose(state))
        _recent = store.retrieve_recent(3)
        allowed = [p for p in proposals if self._allowed(p["name"], state.permissions)]
        return sorted(allowed, key=lambda a: PRIORITY_ORDER.get(a["priority"], 99))

    def _allowed(self, action_name: str, permissions) -> bool:
        required = self.registry.get(action_name, [])
        return all(getattr(permissions, r, False) for r in required)

    def execute(self, action: dict) -> str:
        name = action.get("name")
        if name in {"say", "ask_clarifying"}:
            return action.get("content", "")
        if name == "write_memory":
            return "memory stored"
        messages = [
            {"role": "system", "content": "You are eCole, warm and supportive."},
            {"role": "user", "content": action.get("content", "")},
        ]
        expected_context = sum(len(m["content"]) for m in messages)
        expected_output = action.get("max_tokens", 800)
        task = {
            "type": action.get("type", "general_chat"),
            "expected_context_tokens": expected_context,
            "expected_output_tokens": expected_output,
        }
        return self.llm.generate(task, messages, max_tokens=expected_output)

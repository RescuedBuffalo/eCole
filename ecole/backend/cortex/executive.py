import yaml

from ..state.schema import AgentState
from ..models.llm import LocalLLM
from ..brain import frontal, temporal, limbic, basal_ganglia, parietal, cerebellum
from ..memory import store

PRIORITY_ORDER = {"comfort": 0, "clarify": 1, "plan": 2, "routine": 3}


class ExecutiveController:
    def __init__(self, registry_path: str = "ecole/action_registry.yaml"):
        with open(registry_path, "r") as fh:
            self.registry = yaml.safe_load(fh)
        self.llm = LocalLLM()
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
        return self.llm.generate(action.get("content", ""))

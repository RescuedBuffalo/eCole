from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Permissions:
    speak: bool = True
    memory_read: bool = True
    memory_write: bool = True
    plan: bool = True
    routine: bool = False

    @classmethod
    def default(cls) -> "Permissions":
        return cls()


@dataclass
class Goal:
    description: str


@dataclass
class WorkingMemoryItem:
    content: str
    timestamp: str


@dataclass
class AgentState:
    last_message: str = ""
    mood: Dict[str, float] = field(
        default_factory=lambda: {"valence": 0.0, "arousal": 0.0}
    )
    goals: List[Goal] = field(default_factory=list)
    permissions: Permissions = field(default_factory=Permissions)
    working_memory: List[WorkingMemoryItem] = field(default_factory=list)

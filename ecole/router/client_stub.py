"""Router client protocol stub."""

from __future__ import annotations

from typing import Any, Protocol


class RouterClient(Protocol):
    """Interface for LLM routing."""

    def generate(self, task: str, **kwargs: Any) -> str:  # pragma: no cover - interface
        """Generate a string response for the given task."""
        raise NotImplementedError

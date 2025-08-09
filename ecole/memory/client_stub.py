"""Memory client protocol stubs."""

from __future__ import annotations

from typing import Any, Protocol


class MemoryClient(Protocol):
    """Interface for memory operations."""

    def save(
        self, kind: str, content: str, **kwargs: Any
    ) -> str:  # pragma: no cover - interface
        """Save content and return an identifier."""
        raise NotImplementedError

    def query(
        self, query: str, kind: str, k: int = 3
    ) -> list[dict[str, Any]]:  # pragma: no cover - interface
        """Query memory and return results."""
        raise NotImplementedError

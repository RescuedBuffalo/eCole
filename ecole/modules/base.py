"""Module interface."""

from __future__ import annotations

from typing import Protocol

from ..core.interfaces import ModuleProposal
from ..core.run_context import RunContext


class Module(Protocol):
    """Protocol for brain modules."""

    module_id: str

    def propose(
        self, ctx: RunContext
    ) -> ModuleProposal:  # pragma: no cover - interface
        """Return a proposal for the next action."""
        ...

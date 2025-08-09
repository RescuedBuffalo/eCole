"""Typed interfaces and data contracts used across eCole."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal, TypedDict
from uuid import uuid4


class ModuleProposal(TypedDict):
    """Proposal from a module for an action to execute."""

    module_id: str
    action_id: str
    payload: dict[str, Any]
    utility_est: float
    cost_est: float
    confidence: float
    rationale_log: str


@dataclass(slots=True)
class Decision:
    """Represents a selection among module proposals."""

    run_id: str
    proposals: list[ModuleProposal]
    selected_index: int | None
    reason: str
    ts: datetime


@dataclass(slots=True)
class ActionRequest:
    """Request to execute an action."""

    run_id: str
    actor: str
    action_id: str
    payload: dict[str, Any]


@dataclass(slots=True)
class ActionResult:
    """Result of executing an action."""

    status: Literal["ok", "denied", "error"]
    action_id: str
    message: str
    data: dict[str, Any] | None = None
    denied_reason: str | None = None


@dataclass(slots=True)
class DecisionLogEntry:
    """Entry in the decision log."""

    run_id: str
    action_id: str
    actor: str
    allowed: bool
    reason: str
    used_memory_refs: list[str]
    ts: datetime


def now_utc() -> datetime:
    """Return the current UTC time."""

    return datetime.now(tz=timezone.utc)


def new_run_id() -> str:
    """Generate a new run identifier."""

    return str(uuid4())

"""Run context utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .decision_log import DecisionLogger
from .interfaces import new_run_id, now_utc


@dataclass
class RunContext:
    """Context for a single run/session."""

    run_id: str
    start_ts: datetime
    logger: DecisionLogger

    @classmethod
    def new(cls) -> "RunContext":
        """Create a new run context."""

        return cls(run_id=new_run_id(), start_ts=now_utc(), logger=DecisionLogger())

"""Structured, user-safe decision log."""

from __future__ import annotations

import json
from dataclasses import asdict

from .interfaces import DecisionLogEntry


class DecisionLogger:
    """Simple in-memory logger for decision entries."""

    def __init__(self) -> None:
        self._entries: list[DecisionLogEntry] = []

    def record(self, entry: DecisionLogEntry) -> None:
        """Record a decision log entry."""

        self._entries.append(entry)

    def last_n(self, n: int) -> list[DecisionLogEntry]:
        """Return the last *n* entries."""

        return self._entries[-n:]

    def to_json(self) -> str:
        """Serialize entries to a JSON string."""

        return json.dumps([asdict(e) for e in self._entries], default=str)

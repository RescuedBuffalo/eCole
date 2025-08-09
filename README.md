eCole v0.01 – Walking Skeleton
==============================

This repository hosts the early "walking skeleton" for eCole, a brain‑inspired
personal OS AI. The Day 1–2 milestone establishes the core package layout,
typed contracts, a permissioned action registry, and minimal console demo.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pre-commit install
pytest -q
python -m ecole.ui.console_stub
```

## Execution Policy

`ACTION_REGISTRY.yaml` controls which actors may execute actions. The default
`execution_policy` is `centralized`, meaning only the `executive` actor may
perform actions. To allow an action's owner to execute it, change the policy to
`owner_allow`.

## Privacy

Decision logs store only user‑safe summaries and metadata—no raw chain of
thought or sensitive content is persisted.

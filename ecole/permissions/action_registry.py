"""Action registry loading, validation, and permission checks."""

from __future__ import annotations

from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

ALLOWED_OWNERS = {
    "executive",
    "temporal",
    "frontal",
    "parietal",
    "limbic",
    "cerebellum",
}
ParamType = Literal[
    "string",
    "integer",
    "boolean",
    "object",
    "list[string]",
    "list[integer]",
    "enum",
]


class ParamDef(BaseModel):
    type: ParamType
    required: bool = False
    default: Any | None = None
    values: list[str] | None = None
    min: int | None = None
    max: int | None = None

    @field_validator("values")
    @classmethod
    def _validate_values(cls, v: list[str] | None, info: Field) -> list[str] | None:
        if info.data.get("type") == "enum" and not v:
            raise ValueError("enum params require 'values'")
        return v


class Permissions(BaseModel):
    requires_user_consult: bool
    pii_write: bool
    pii_read: bool
    editable_by_user: bool


class ActionDef(BaseModel):
    id: str
    owner: str
    params: dict[str, ParamDef]
    permissions: Permissions

    @field_validator("id")
    @classmethod
    def _check_id(cls, v: str) -> str:
        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-.")
        if not set(v) <= allowed_chars:
            raise ValueError("id must be kebab or dot case")
        return v

    @field_validator("owner")
    @classmethod
    def _check_owner(cls, v: str) -> str:
        if v not in ALLOWED_OWNERS:
            raise ValueError("invalid owner")
        return v


class ActionRegistry(BaseModel):
    version: Any
    execution_policy: Literal["centralized", "owner_allow"] = "centralized"
    actions: list[ActionDef]

    @model_validator(mode="after")
    def _unique_ids(self) -> "ActionRegistry":
        ids = [a.id for a in self.actions]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate action id")
        return self

    @classmethod
    def from_yaml(cls, path: str = "ACTION_REGISTRY.yaml") -> "ActionRegistry":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)

    def get(self, action_id: str) -> ActionDef:
        for action in self.actions:
            if action.id == action_id:
                return action
        raise KeyError(action_id)

    def all_actions(self) -> list[str]:
        return [a.id for a in self.actions]

    def validate_payload(self, action_id: str, payload: dict[str, Any]) -> None:
        action = self.get(action_id)
        for key, param in action.params.items():
            if key not in payload:
                if param.required:
                    raise ValueError(f"params.{key}: missing required param")
                continue
            value = payload[key]
            t = param.type
            error_prefix = f"params.{key}:"
            if t == "string":
                if not isinstance(value, str):
                    raise ValueError(f"{error_prefix} expected string")
            elif t == "integer":
                if not isinstance(value, int):
                    raise ValueError(f"{error_prefix} expected integer")
                if param.min is not None and value < param.min:
                    raise ValueError(f"{error_prefix} < min {param.min}")
                if param.max is not None and value > param.max:
                    raise ValueError(f"{error_prefix} > max {param.max}")
            elif t == "boolean":
                if not isinstance(value, bool):
                    raise ValueError(f"{error_prefix} expected boolean")
            elif t == "object":
                if not isinstance(value, dict):
                    raise ValueError(f"{error_prefix} expected object")
            elif t == "list[string]":
                if not (
                    isinstance(value, list) and all(isinstance(i, str) for i in value)
                ):
                    raise ValueError(f"{error_prefix} expected list of strings")
            elif t == "list[integer]":
                if not (
                    isinstance(value, list) and all(isinstance(i, int) for i in value)
                ):
                    raise ValueError(f"{error_prefix} expected list of integers")
            elif t == "enum":
                if not isinstance(value, str):
                    raise ValueError(f"{error_prefix} expected string for enum")
                if param.values and value not in param.values:
                    raise ValueError(f"{error_prefix} invalid enum value")
            else:
                raise ValueError(f"{error_prefix} unknown type {t}")
        for key in payload:
            if key not in action.params:
                raise ValueError(f"params.{key}: unknown param")

    def is_allowed(self, actor: str, action_id: str) -> tuple[bool, str]:
        action = self.get(action_id)
        if self.execution_policy == "centralized":
            if actor == "executive":
                return True, "allowed"
            return False, f"centralized execution (actor={actor})"
        if self.execution_policy == "owner_allow":
            if actor in {"executive", action.owner}:
                return True, "allowed"
            return False, f"owner {action.owner} or executive required (actor={actor})"
        return False, "unknown policy"

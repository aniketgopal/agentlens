from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Callable


Masker = Callable[[dict[str, Any]], dict[str, Any]]


def default_mask_payload(payload: dict[str, Any]) -> dict[str, Any]:
    cloned = deepcopy(payload)
    return _walk_and_mask(cloned)


def _walk_and_mask(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _walk_and_mask(_mask_scalar(key, nested)) for key, nested in value.items()}
    if isinstance(value, list):
        return [_walk_and_mask(item) for item in value]
    return _mask_scalar("", value)


def _mask_scalar(key: str, value: Any) -> Any:
    if not isinstance(value, str):
        return value
    if "password" in key.lower():
        return "***"
    value = re.sub(r"([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", r"\1***@\2", value)
    value = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "***", value)
    value = re.sub(r"\b\d{10,16}\b", "***", value)
    return value

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class StepPayload:
    step_id: str
    parent_step_id: str | None
    type: str
    name: str
    status: str
    input: dict[str, Any]
    output: dict[str, Any] = field(default_factory=dict)
    model: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, Any] = field(default_factory=dict)
    latency_ms: int | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] | None = None

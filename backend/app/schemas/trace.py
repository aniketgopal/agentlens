from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class IngestStepRequest(BaseModel):
    step_id: str
    parent_step_id: str | None = None
    type: str
    name: str
    status: str
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    model: dict[str, Any] = Field(default_factory=dict)
    usage: dict[str, Any] = Field(default_factory=dict)
    latency_ms: int | None = None
    started_at: datetime
    ended_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: dict[str, Any] | None = None


class IngestStepResponse(BaseModel):
    step_id: str
    run_id: str

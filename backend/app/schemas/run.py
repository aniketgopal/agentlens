from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CreateRunRequest(BaseModel):
    project_id: str
    run_id: str
    name: str
    environment: str = "local"
    input: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime


class EndRunRequest(BaseModel):
    status: str
    output: dict[str, Any] = Field(default_factory=dict)
    ended_at: datetime


class RunSummaryResponse(BaseModel):
    run_id: str
    project_id: str
    name: str
    status: str
    environment: str
    duration_ms: int | None = None
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    error_count: int = 0
    security_finding_count: int = 0
    started_at: datetime
    ended_at: datetime | None = None


class RunDetailResponse(RunSummaryResponse):
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    steps: list[dict[str, Any]] = Field(default_factory=list)

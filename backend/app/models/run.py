from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RunRecord(BaseModel):
    id: str
    project_id: str
    name: str
    environment: str = "local"
    status: str = "running"
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime
    ended_at: datetime | None = None
    duration_ms: int | None = None
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    error_count: int = 0
    security_finding_count: int = 0
    created_at: datetime

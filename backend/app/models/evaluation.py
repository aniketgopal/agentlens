from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EvaluationRecord(BaseModel):
    id: str
    project_id: str
    run_id: str
    status: str = "completed"
    score: float
    passed: bool
    metrics: dict[str, Any] = Field(default_factory=dict)
    failures: list[dict[str, Any]] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

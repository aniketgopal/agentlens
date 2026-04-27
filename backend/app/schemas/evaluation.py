from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RunEvaluationRequest(BaseModel):
    run_id: str
    required_terms: list[str] = Field(default_factory=list)
    forbidden_terms: list[str] = Field(default_factory=list)
    required_output_keys: list[str] = Field(default_factory=list)


class EvaluationResponse(BaseModel):
    evaluation_id: str
    project_id: str
    run_id: str
    status: str
    score: float
    passed: bool
    metrics: dict[str, float]
    failures: list[dict[str, str]]
    config: dict[str, list[str]]
    created_at: datetime

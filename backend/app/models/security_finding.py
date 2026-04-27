from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SecurityFindingRecord(BaseModel):
    id: str
    project_id: str
    run_id: str
    step_id: str | None = None
    rule_id: str
    severity: str
    category: str
    message: str
    evidence: str
    status: str = "open"
    created_at: datetime

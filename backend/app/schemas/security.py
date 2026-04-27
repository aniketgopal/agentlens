from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SecurityFindingResponse(BaseModel):
    finding_id: str
    project_id: str
    run_id: str
    step_id: str | None = None
    rule_id: str
    severity: str
    category: str
    message: str
    evidence: str
    status: str
    created_at: datetime

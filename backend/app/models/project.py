from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProjectRecord(BaseModel):
    id: str
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ApiKeyRecord(BaseModel):
    id: str
    project_id: str
    key_hash: str
    prefix: str
    created_at: datetime
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None

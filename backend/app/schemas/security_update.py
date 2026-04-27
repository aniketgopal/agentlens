from __future__ import annotations

from pydantic import BaseModel


class UpdateSecurityFindingRequest(BaseModel):
    status: str

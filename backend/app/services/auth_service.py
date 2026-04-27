from __future__ import annotations

from fastapi import Header, HTTPException, status

from app.core.security import hash_api_key
from app.models.common import utc_now
from app.repositories.mongo_api_key_repository import MongoApiKeyRepository


def require_project_api_key(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    raw_key = authorization.removeprefix("Bearer ").strip()
    repo = MongoApiKeyRepository()
    record = repo.find_active_by_hash(hash_api_key(raw_key))
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    repo.touch_last_used(record.id, utc_now())
    return record.project_id

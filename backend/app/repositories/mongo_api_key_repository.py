from __future__ import annotations

from datetime import datetime

from app.models.api_key import ApiKeyRecord
from app.repositories.mongo import MongoRepository


class MongoApiKeyRepository(MongoRepository):
    collection_name = "api_keys"

    def create(self, api_key: ApiKeyRecord) -> ApiKeyRecord:
        self.collection(self.collection_name).insert_one(
            {
                "_id": api_key.id,
                "project_id": api_key.project_id,
                "key_hash": api_key.key_hash,
                "prefix": api_key.prefix,
                "created_at": api_key.created_at,
                "last_used_at": api_key.last_used_at,
                "revoked_at": api_key.revoked_at,
            }
        )
        return api_key

    def find_active_by_hash(self, key_hash: str) -> ApiKeyRecord | None:
        doc = self.collection(self.collection_name).find_one(
            {"key_hash": key_hash, "revoked_at": None}
        )
        if not doc:
            return None
        return ApiKeyRecord(
            id=doc["_id"],
            project_id=doc["project_id"],
            key_hash=doc["key_hash"],
            prefix=doc["prefix"],
            created_at=doc["created_at"],
            last_used_at=doc.get("last_used_at"),
            revoked_at=doc.get("revoked_at"),
        )

    def touch_last_used(self, key_id: str, used_at: datetime) -> None:
        self.collection(self.collection_name).update_one(
            {"_id": key_id},
            {"$set": {"last_used_at": used_at}},
        )

from __future__ import annotations

from app.models.run import RunRecord
from app.repositories.mongo import MongoRepository


class MongoRunRepository(MongoRepository):
    collection_name = "runs"

    def create(self, run: RunRecord) -> RunRecord:
        self.collection(self.collection_name).insert_one(
            {"_id": run.id, **run.model_dump(exclude={"id"})}
        )
        return run

    def update(self, run: RunRecord) -> RunRecord:
        self.collection(self.collection_name).update_one(
            {"_id": run.id},
            {"$set": run.model_dump(exclude={"id"})},
        )
        return run

    def get(self, run_id: str) -> RunRecord | None:
        doc = self.collection(self.collection_name).find_one({"_id": run_id})
        if not doc:
            return None
        return RunRecord(id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"})

    def list(self, project_id: str, status: str | None = None) -> list[RunRecord]:
        query: dict[str, object] = {"project_id": project_id}
        if status:
            query["status"] = status
        docs = self.collection(self.collection_name).find(query).sort("started_at", -1)
        return [
            RunRecord(id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"})
            for doc in docs
        ]

from __future__ import annotations

from app.models.trace_step import TraceStepRecord
from app.repositories.mongo import MongoRepository


class MongoTraceRepository(MongoRepository):
    collection_name = "trace_steps"

    def create(self, step: TraceStepRecord) -> TraceStepRecord:
        self.collection(self.collection_name).insert_one(
            {"_id": step.id, **step.model_dump(exclude={"id"})}
        )
        return step

    def list_for_run(self, run_id: str) -> list[TraceStepRecord]:
        docs = self.collection(self.collection_name).find({"run_id": run_id}).sort(
            "started_at", 1
        )
        return [
            TraceStepRecord(
                id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}
            )
            for doc in docs
        ]

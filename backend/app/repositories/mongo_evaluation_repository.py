from __future__ import annotations

from app.models.evaluation import EvaluationRecord
from app.repositories.mongo import MongoRepository


class MongoEvaluationRepository(MongoRepository):
    collection_name = "evaluations"

    def create(self, evaluation: EvaluationRecord) -> EvaluationRecord:
        self.collection(self.collection_name).insert_one(
            {"_id": evaluation.id, **evaluation.model_dump(exclude={"id"})}
        )
        return evaluation

    def list(self, project_id: str, run_id: str | None = None) -> list[EvaluationRecord]:
        query: dict[str, object] = {"project_id": project_id}
        if run_id:
            query["run_id"] = run_id
        docs = self.collection(self.collection_name).find(query).sort("created_at", -1)
        return [
            EvaluationRecord(
                id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}
            )
            for doc in docs
        ]

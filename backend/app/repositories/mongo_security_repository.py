from __future__ import annotations

from app.models.security_finding import SecurityFindingRecord
from app.repositories.mongo import MongoRepository


class MongoSecurityRepository(MongoRepository):
    collection_name = "security_findings"

    def create_many(
        self, findings: list[SecurityFindingRecord]
    ) -> list[SecurityFindingRecord]:
        if not findings:
            return findings
        self.collection(self.collection_name).insert_many(
            [{"_id": finding.id, **finding.model_dump(exclude={"id"})} for finding in findings]
        )
        return findings

    def list(
        self,
        project_id: str,
        severity: str | None = None,
        status: str | None = None,
        run_id: str | None = None,
    ) -> list[SecurityFindingRecord]:
        query: dict[str, object] = {"project_id": project_id}
        if severity:
            query["severity"] = severity
        if status:
            query["status"] = status
        if run_id:
            query["run_id"] = run_id

        docs = self.collection(self.collection_name).find(query).sort("created_at", -1)
        return [
            SecurityFindingRecord(
                id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}
            )
            for doc in docs
        ]

    def count_for_run(self, run_id: str) -> int:
        return int(self.collection(self.collection_name).count_documents({"run_id": run_id}))

    def update_status(self, finding_id: str, status: str) -> SecurityFindingRecord | None:
        self.collection(self.collection_name).update_one(
            {"_id": finding_id},
            {"$set": {"status": status}},
        )
        doc = self.collection(self.collection_name).find_one({"_id": finding_id})
        if not doc:
            return None
        return SecurityFindingRecord(
            id=doc["_id"], **{k: v for k, v in doc.items() if k != "_id"}
        )

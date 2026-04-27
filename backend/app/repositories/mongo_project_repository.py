from __future__ import annotations

from app.models.project import ProjectRecord
from app.repositories.mongo import MongoRepository


class MongoProjectRepository(MongoRepository):
    collection_name = "projects"

    def create(self, project: ProjectRecord) -> ProjectRecord:
        self.collection(self.collection_name).insert_one(
            {
                "_id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        )
        return project

    def get(self, project_id: str) -> ProjectRecord | None:
        doc = self.collection(self.collection_name).find_one({"_id": project_id})
        if not doc:
            return None
        return ProjectRecord(
            id=doc["_id"],
            name=doc["name"],
            description=doc.get("description"),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )

    def list(self) -> list[ProjectRecord]:
        docs = self.collection(self.collection_name).find({}).sort("created_at", -1)
        return [
            ProjectRecord(
                id=doc["_id"],
                name=doc["name"],
                description=doc.get("description"),
                created_at=doc["created_at"],
                updated_at=doc["updated_at"],
            )
            for doc in docs
        ]

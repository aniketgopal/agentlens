from __future__ import annotations

import secrets

from app.core.security import generate_api_key, hash_api_key
from app.models.api_key import ApiKeyRecord
from app.models.common import utc_now
from app.models.project import ProjectRecord
from app.repositories.mongo_api_key_repository import MongoApiKeyRepository
from app.repositories.mongo_project_repository import MongoProjectRepository
from app.schemas.project import CreateProjectRequest, ProjectListItemResponse, ProjectResponse


class ProjectService:
    def __init__(self) -> None:
        self.projects = MongoProjectRepository()
        self.api_keys = MongoApiKeyRepository()

    def create_project(self, payload: CreateProjectRequest) -> ProjectResponse:
        now = utc_now()
        project = ProjectRecord(
            id=f"proj_{secrets.token_hex(6)}",
            name=payload.name,
            description=payload.description,
            created_at=now,
            updated_at=now,
        )
        self.projects.create(project)
        return ProjectResponse(
            project_id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
        )

    def list_projects(self) -> list[ProjectListItemResponse]:
        projects = self.projects.list()
        return [
            ProjectListItemResponse(
                project_id=project.id,
                name=project.name,
                description=project.description,
                created_at=project.created_at,
            )
            for project in projects
        ]

    def create_api_key(self, project_id: str) -> dict[str, str]:
        if self.projects.get(project_id) is None:
            raise ValueError("Project not found")
        raw_key = generate_api_key()
        record = ApiKeyRecord(
            id=f"key_{secrets.token_hex(6)}",
            project_id=project_id,
            key_hash=hash_api_key(raw_key),
            prefix=raw_key[:12],
            created_at=utc_now(),
        )
        self.api_keys.create(record)
        return {"api_key": raw_key, "key_id": record.id}

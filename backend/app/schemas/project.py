from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str | None = None
    created_at: datetime


class ProjectListItemResponse(ProjectResponse):
    pass

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.common import ApiResponse
from app.schemas.project import CreateProjectRequest
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.get("")
def list_projects() -> ApiResponse:
    service = ProjectService()
    return ApiResponse(data=service.list_projects())


@router.post("")
def create_project(payload: CreateProjectRequest) -> ApiResponse:
    service = ProjectService()
    return ApiResponse(data=service.create_project(payload))


@router.post("/{project_id}/api-keys")
def create_api_key(project_id: str) -> ApiResponse:
    service = ProjectService()
    try:
        return ApiResponse(data=service.create_api_key(project_id))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

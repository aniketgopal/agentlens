from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.schemas.common import ApiResponse
from app.schemas.run import CreateRunRequest, EndRunRequest
from app.services.auth_service import require_project_api_key
from app.services.trace_service import TraceService

router = APIRouter(prefix="/api/v1/runs", tags=["runs"])


@router.post("")
def create_run(
    payload: CreateRunRequest,
    project_id: str = Depends(require_project_api_key),
) -> ApiResponse:
    service = TraceService()
    return ApiResponse(data=service.create_run(payload, authenticated_project_id=project_id))


@router.patch("/{run_id}/end")
def end_run(
    run_id: str,
    payload: EndRunRequest,
    project_id: str = Depends(require_project_api_key),
) -> ApiResponse:
    service = TraceService()
    return ApiResponse(data=service.end_run(run_id, payload, authenticated_project_id=project_id))


@router.get("")
def list_runs(
    project_id: str = Query(...),
    status: str | None = Query(default=None),
) -> ApiResponse:
    service = TraceService()
    return ApiResponse(data=service.list_runs(project_id=project_id, status=status))


@router.get("/{run_id}")
def get_run(run_id: str) -> ApiResponse:
    service = TraceService()
    return ApiResponse(data=service.get_run_detail(run_id))

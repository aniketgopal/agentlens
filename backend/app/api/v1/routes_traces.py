from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.common import ApiResponse
from app.schemas.trace import IngestStepRequest
from app.services.auth_service import require_project_api_key
from app.services.trace_service import TraceService

router = APIRouter(prefix="/api/v1/runs", tags=["traces"])


@router.post("/{run_id}/steps")
def ingest_step(
    run_id: str,
    payload: IngestStepRequest,
    project_id: str = Depends(require_project_api_key),
) -> ApiResponse:
    service = TraceService()
    return ApiResponse(data=service.ingest_step(run_id, payload, authenticated_project_id=project_id))

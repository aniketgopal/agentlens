from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.common import ApiResponse
from app.schemas.evaluation import RunEvaluationRequest
from app.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/api/v1/evaluations", tags=["evaluations"])


@router.post("/run")
def run_evaluation(payload: RunEvaluationRequest) -> ApiResponse:
    service = EvaluationService()
    return ApiResponse(data=service.run_evaluation(payload))


@router.get("")
def list_evaluations(
    project_id: str = Query(...),
    run_id: str | None = Query(default=None),
) -> ApiResponse:
    service = EvaluationService()
    return ApiResponse(data=service.list_evaluations(project_id=project_id, run_id=run_id))

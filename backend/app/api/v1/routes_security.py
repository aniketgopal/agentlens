from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas.common import ApiResponse
from app.schemas.security_update import UpdateSecurityFindingRequest
from app.services.security_service import SecurityService

router = APIRouter(prefix="/api/v1/security", tags=["security"])


@router.get("/findings")
def list_security_findings(
    project_id: str = Query(...),
    severity: str | None = Query(default=None),
    status: str | None = Query(default=None),
    run_id: str | None = Query(default=None),
) -> ApiResponse:
    service = SecurityService()
    return ApiResponse(
        data=service.list_findings(
            project_id=project_id,
            severity=severity,
            status=status,
            run_id=run_id,
        )
    )


@router.patch("/findings/{finding_id}")
def update_security_finding(
    finding_id: str,
    payload: UpdateSecurityFindingRequest,
) -> ApiResponse:
    service = SecurityService()
    return ApiResponse(
        data=service.update_finding_status(finding_id=finding_id, status=payload.status)
    )

from __future__ import annotations

from fastapi import HTTPException

from app.repositories.mongo_security_repository import MongoSecurityRepository
from app.schemas.security import SecurityFindingResponse


class SecurityService:
    def __init__(self) -> None:
        self.findings = MongoSecurityRepository()

    def list_findings(
        self,
        *,
        project_id: str,
        severity: str | None = None,
        status: str | None = None,
        run_id: str | None = None,
    ) -> list[SecurityFindingResponse]:
        findings = self.findings.list(
            project_id=project_id,
            severity=severity,
            status=status,
            run_id=run_id,
        )
        return [
            SecurityFindingResponse(
                finding_id=finding.id,
                project_id=finding.project_id,
                run_id=finding.run_id,
                step_id=finding.step_id,
                rule_id=finding.rule_id,
                severity=finding.severity,
                category=finding.category,
                message=finding.message,
                evidence=finding.evidence,
                status=finding.status,
                created_at=finding.created_at,
            )
            for finding in findings
        ]

    def update_finding_status(
        self, *, finding_id: str, status: str
    ) -> SecurityFindingResponse:
        if status not in {"open", "false_positive", "resolved"}:
            raise HTTPException(status_code=400, detail="Invalid finding status")
        finding = self.findings.update_status(finding_id, status)
        if finding is None:
            raise HTTPException(status_code=404, detail="Finding not found")
        return SecurityFindingResponse(
            finding_id=finding.id,
            project_id=finding.project_id,
            run_id=finding.run_id,
            step_id=finding.step_id,
            rule_id=finding.rule_id,
            severity=finding.severity,
            category=finding.category,
            message=finding.message,
            evidence=finding.evidence,
            status=finding.status,
            created_at=finding.created_at,
        )

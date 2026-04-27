from __future__ import annotations

from fastapi import HTTPException, status

from app.models.common import ensure_utc, utc_now
from app.models.run import RunRecord
from app.models.trace_step import TraceStepRecord
from app.repositories.mongo_project_repository import MongoProjectRepository
from app.repositories.mongo_run_repository import MongoRunRepository
from app.repositories.mongo_security_repository import MongoSecurityRepository
from app.repositories.mongo_trace_repository import MongoTraceRepository
from app.schemas.run import (
    CreateRunRequest,
    EndRunRequest,
    RunDetailResponse,
    RunSummaryResponse,
)
from app.schemas.trace import IngestStepRequest, IngestStepResponse
from app.services.masking_service import MaskingService
from app.services.security_scanner import SecurityScanner


class TraceService:
    def __init__(self) -> None:
        self.projects = MongoProjectRepository()
        self.runs = MongoRunRepository()
        self.steps = MongoTraceRepository()
        self.security_findings = MongoSecurityRepository()
        self.masking = MaskingService()
        self.security_scanner = SecurityScanner()

    def create_run(self, payload: CreateRunRequest, authenticated_project_id: str) -> dict[str, str]:
        if payload.project_id != authenticated_project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project mismatch for API key",
            )
        if self.projects.get(payload.project_id) is None:
            raise HTTPException(status_code=404, detail="Project not found")

        masked_input = self.masking.sanitize_and_validate("run.input", payload.input)
        masked_metadata = self.masking.sanitize_and_validate("run.metadata", payload.metadata)

        run = RunRecord(
            id=payload.run_id,
            project_id=payload.project_id,
            name=payload.name,
            environment=payload.environment,
            input=masked_input,
            metadata=masked_metadata,
            started_at=payload.started_at,
            created_at=utc_now(),
        )
        self.runs.create(run)
        return {"run_id": run.id}

    def ingest_step(
        self,
        run_id: str,
        payload: IngestStepRequest,
        authenticated_project_id: str,
    ) -> IngestStepResponse:
        run = self.runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")
        if run.project_id != authenticated_project_id:
            raise HTTPException(status_code=403, detail="Project mismatch for API key")

        masked_input = self.masking.sanitize_and_validate("step.input", payload.input)
        masked_output = self.masking.sanitize_and_validate("step.output", payload.output)
        masked_model = self.masking.sanitize_and_validate("step.model", payload.model)
        masked_usage = self.masking.sanitize_and_validate("step.usage", payload.usage)
        masked_metadata = self.masking.sanitize_and_validate("step.metadata", payload.metadata)
        masked_error = self.masking.sanitize_and_validate("step.error", payload.error)

        step = TraceStepRecord(
            id=payload.step_id,
            run_id=run_id,
            project_id=run.project_id,
            parent_step_id=payload.parent_step_id,
            type=payload.type,
            name=payload.name,
            status=payload.status,
            input=masked_input,
            output=masked_output,
            model=masked_model,
            usage=masked_usage,
            latency_ms=payload.latency_ms,
            started_at=payload.started_at,
            ended_at=payload.ended_at,
            metadata=masked_metadata,
            error=masked_error,
        )
        self.steps.create(step)

        findings = self.security_scanner.scan_payloads(
            project_id=run.project_id,
            run_id=run_id,
            step_id=step.id,
            payloads=[
                ("step.input", masked_input),
                ("step.output", masked_output),
                ("step.error", masked_error),
            ],
        )
        self.security_findings.create_many(findings)

        total_tokens = run.total_tokens + int(masked_usage.get("total_tokens", 0) or 0)
        error_count = run.error_count + (1 if payload.status == "failed" else 0)
        run.total_tokens = total_tokens
        run.error_count = error_count
        run.security_finding_count = self.security_findings.count_for_run(run_id)
        self.runs.update(run)

        return IngestStepResponse(step_id=step.id, run_id=run_id)

    def end_run(
        self,
        run_id: str,
        payload: EndRunRequest,
        authenticated_project_id: str,
    ) -> dict[str, str]:
        run = self.runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")
        if run.project_id != authenticated_project_id:
            raise HTTPException(status_code=403, detail="Project mismatch for API key")

        masked_output = self.masking.sanitize_and_validate("run.output", payload.output)
        run.status = payload.status
        run.output = masked_output
        run.ended_at = payload.ended_at
        started_at = ensure_utc(run.started_at)
        ended_at = ensure_utc(payload.ended_at)
        run.duration_ms = int((ended_at - started_at).total_seconds() * 1000)

        findings = self.security_scanner.scan_payloads(
            project_id=run.project_id,
            run_id=run.id,
            step_id=None,
            payloads=[("run.output", masked_output)],
        )
        self.security_findings.create_many(findings)
        run.security_finding_count = self.security_findings.count_for_run(run.id)
        self.runs.update(run)
        return {"run_id": run.id, "status": run.status}

    def list_runs(self, project_id: str, status: str | None = None) -> list[RunSummaryResponse]:
        runs = self.runs.list(project_id=project_id, status=status)
        return [
            RunSummaryResponse(
                run_id=run.id,
                project_id=run.project_id,
                name=run.name,
                status=run.status,
                environment=run.environment,
                duration_ms=run.duration_ms,
                total_tokens=run.total_tokens,
                total_cost_usd=run.total_cost_usd,
                error_count=run.error_count,
                security_finding_count=run.security_finding_count,
                started_at=run.started_at,
                ended_at=run.ended_at,
            )
            for run in runs
        ]

    def get_run_detail(self, run_id: str) -> RunDetailResponse:
        run = self.runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")
        steps = self.steps.list_for_run(run_id)
        return RunDetailResponse(
            run_id=run.id,
            project_id=run.project_id,
            name=run.name,
            status=run.status,
            environment=run.environment,
            duration_ms=run.duration_ms,
            total_tokens=run.total_tokens,
            total_cost_usd=run.total_cost_usd,
            error_count=run.error_count,
            security_finding_count=run.security_finding_count,
            started_at=run.started_at,
            ended_at=run.ended_at,
            input=run.input,
            output=run.output,
            metadata=run.metadata,
            steps=[step.model_dump(mode="json") | {"step_id": step.id} for step in steps],
        )

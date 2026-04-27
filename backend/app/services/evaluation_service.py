from __future__ import annotations

import secrets
from typing import Any

from fastapi import HTTPException

from app.models.common import utc_now
from app.models.evaluation import EvaluationRecord
from app.repositories.mongo_evaluation_repository import MongoEvaluationRepository
from app.repositories.mongo_run_repository import MongoRunRepository
from app.schemas.evaluation import EvaluationResponse, RunEvaluationRequest


class EvaluationService:
    def __init__(self) -> None:
        self.runs = MongoRunRepository()
        self.evaluations = MongoEvaluationRepository()

    def run_evaluation(self, payload: RunEvaluationRequest) -> EvaluationResponse:
        run = self.runs.get(payload.run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")

        output_text = _stringify(run.output).lower()
        failures: list[dict[str, str]] = []
        metrics: dict[str, float] = {}

        if payload.required_terms:
            matched = sum(1 for term in payload.required_terms if term.lower() in output_text)
            metrics["required_terms_coverage"] = matched / len(payload.required_terms)
            for term in payload.required_terms:
                if term.lower() not in output_text:
                    failures.append({"type": "missing_required_term", "value": term})
        else:
            metrics["required_terms_coverage"] = 1.0

        if payload.forbidden_terms:
            clean = sum(
                1 for term in payload.forbidden_terms if term.lower() not in output_text
            )
            metrics["forbidden_terms_compliance"] = clean / len(payload.forbidden_terms)
            for term in payload.forbidden_terms:
                if term.lower() in output_text:
                    failures.append({"type": "forbidden_term_present", "value": term})
        else:
            metrics["forbidden_terms_compliance"] = 1.0

        if payload.required_output_keys:
            present = sum(1 for key in payload.required_output_keys if key in run.output)
            metrics["required_output_keys_coverage"] = present / len(
                payload.required_output_keys
            )
            for key in payload.required_output_keys:
                if key not in run.output:
                    failures.append({"type": "missing_output_key", "value": key})
        else:
            metrics["required_output_keys_coverage"] = 1.0

        score = sum(metrics.values()) / len(metrics)
        passed = len(failures) == 0
        evaluation = EvaluationRecord(
            id=f"eval_{secrets.token_hex(8)}",
            project_id=run.project_id,
            run_id=run.id,
            score=round(score, 4),
            passed=passed,
            metrics={key: round(value, 4) for key, value in metrics.items()},
            failures=failures,
            config={
                "required_terms": payload.required_terms,
                "forbidden_terms": payload.forbidden_terms,
                "required_output_keys": payload.required_output_keys,
            },
            created_at=utc_now(),
        )
        self.evaluations.create(evaluation)
        return _to_response(evaluation)

    def list_evaluations(
        self, *, project_id: str, run_id: str | None = None
    ) -> list[EvaluationResponse]:
        evaluations = self.evaluations.list(project_id=project_id, run_id=run_id)
        return [_to_response(evaluation) for evaluation in evaluations]


def _to_response(evaluation: EvaluationRecord) -> EvaluationResponse:
    return EvaluationResponse(
        evaluation_id=evaluation.id,
        project_id=evaluation.project_id,
        run_id=evaluation.run_id,
        status=evaluation.status,
        score=evaluation.score,
        passed=evaluation.passed,
        metrics=evaluation.metrics,
        failures=evaluation.failures,
        config=evaluation.config,
        created_at=evaluation.created_at,
    )


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_stringify(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_stringify(item) for item in value)
    return str(value)

from app.models.common import utc_now
from app.models.run import RunRecord
from app.repositories.mongo_run_repository import MongoRunRepository
from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation import RunEvaluationRequest


def test_string_evaluation_flow_with_required_and_forbidden_terms(monkeypatch) -> None:
    stored: dict[str, RunRecord] = {}

    class FakeRunRepository:
        def get(self, run_id: str) -> RunRecord | None:
            return stored.get(run_id)

    class FakeEvaluationRepository:
        def create(self, evaluation):
            return evaluation

    monkeypatch.setattr("app.services.evaluation_service.MongoRunRepository", FakeRunRepository)
    monkeypatch.setattr(
        "app.services.evaluation_service.MongoEvaluationRepository",
        FakeEvaluationRepository,
    )

    stored["run_1"] = RunRecord(
        id="run_1",
        project_id="proj_1",
        name="demo",
        output={"answer": "request approved and policy compliant"},
        started_at=utc_now(),
        created_at=utc_now(),
    )

    service = EvaluationService()
    result = service.run_evaluation(
        RunEvaluationRequest(
            run_id="run_1",
            required_terms=["approved"],
            forbidden_terms=["salary promise"],
            required_output_keys=["answer"],
        )
    )

    assert result.passed is True
    assert result.score == 1.0

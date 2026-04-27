from __future__ import annotations

from fastapi import FastAPI

from app.api.v1.routes_projects import router as projects_router
from app.api.v1.routes_evaluations import router as evaluations_router
from app.api.v1.routes_runs import router as runs_router
from app.api.v1.routes_security import router as security_router
from app.api.v1.routes_traces import router as traces_router

app = FastAPI(title="AgentLens API", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(projects_router)
app.include_router(evaluations_router)
app.include_router(runs_router)
app.include_router(traces_router)
app.include_router(security_router)

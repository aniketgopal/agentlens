"use client";

import { useMemo, useState } from "react";

import { EvaluationRecord, RunSummary } from "../../lib/types";

const baseUrl =
  process.env.NEXT_PUBLIC_AGENTLENS_API_BASE_URL ?? "http://localhost:8000";

function toList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function EvaluationManager({
  projectId,
  runs,
  initialEvaluations
}: {
  projectId: string;
  runs: RunSummary[];
  initialEvaluations: EvaluationRecord[];
}) {
  const [selectedRunId, setSelectedRunId] = useState(runs[0]?.run_id ?? "");
  const [requiredTerms, setRequiredTerms] = useState("");
  const [forbiddenTerms, setForbiddenTerms] = useState("");
  const [requiredOutputKeys, setRequiredOutputKeys] = useState("");
  const [evaluations, setEvaluations] = useState(initialEvaluations);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const orderedEvaluations = useMemo(
    () => [...evaluations].sort((left, right) => right.created_at.localeCompare(left.created_at)),
    [evaluations]
  );

  async function runEvaluation() {
    if (!selectedRunId) {
      setError("Select a run first.");
      return;
    }
    setError(null);
    setIsRunning(true);
    try {
      const response = await fetch(`${baseUrl}/api/v1/evaluations/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_id: selectedRunId,
          required_terms: toList(requiredTerms),
          forbidden_terms: toList(forbiddenTerms),
          required_output_keys: toList(requiredOutputKeys)
        })
      });
      if (!response.ok) {
        throw new Error(`Evaluation failed: ${response.status}`);
      }
      const payload = await response.json();
      setEvaluations((current) => [payload.data as EvaluationRecord, ...current]);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unknown error");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="section-label">Run Evaluation</div>
        <div className="project-form">
          <label className="control-group">
            <span className="muted">Run</span>
            <select
              className="control-input"
              value={selectedRunId}
              onChange={(event) => setSelectedRunId(event.target.value)}
            >
              {runs.map((run) => (
                <option key={run.run_id} value={run.run_id}>
                  {run.name} · {run.run_id}
                </option>
              ))}
            </select>
          </label>
          <label className="control-group">
            <span className="muted">Required terms</span>
            <input
              className="control-input"
              value={requiredTerms}
              onChange={(event) => setRequiredTerms(event.target.value)}
              placeholder="approved, policy compliant"
            />
          </label>
          <label className="control-group">
            <span className="muted">Forbidden terms</span>
            <input
              className="control-input"
              value={forbiddenTerms}
              onChange={(event) => setForbiddenTerms(event.target.value)}
              placeholder="confidential terms, private notes"
            />
          </label>
          <label className="control-group">
            <span className="muted">Required output keys</span>
            <input
              className="control-input"
              value={requiredOutputKeys}
              onChange={(event) => setRequiredOutputKeys(event.target.value)}
              placeholder="answer, result"
            />
          </label>
          <button
            type="button"
            className="tab-button"
            onClick={runEvaluation}
            disabled={isRunning}
          >
            {isRunning ? "Running..." : "Run evaluation"}
          </button>
        </div>
        {error ? <p className="muted" style={{ marginTop: 12 }}>{error}</p> : null}
      </section>

      {orderedEvaluations.length === 0 ? (
        <section className="card">
          <h3>No evaluations yet</h3>
          <p className="muted">Run an evaluation against a stored trace to see results here.</p>
        </section>
      ) : (
        <section className="grid">
          {orderedEvaluations.map((evaluation) => (
            <div key={evaluation.evaluation_id} className="card">
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <div>
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <div className={`badge ${evaluation.passed ? "success" : "failed"}`}>
                      {evaluation.passed ? "passed" : "failed"}
                    </div>
                    <div className="badge">{evaluation.run_id}</div>
                  </div>
                  <h3 style={{ marginBottom: 8 }}>Score: {evaluation.score}</h3>
                </div>
                <div className="muted">{evaluation.created_at}</div>
              </div>
              <div className="muted">Project: {projectId}</div>
              <pre>{JSON.stringify(evaluation.metrics, null, 2)}</pre>
              {evaluation.failures.length > 0 ? (
                <>
                  <div className="section-label" style={{ marginTop: 14 }}>Failures</div>
                  <pre>{JSON.stringify(evaluation.failures, null, 2)}</pre>
                </>
              ) : null}
              <div className="section-label" style={{ marginTop: 14 }}>Config</div>
              <pre>{JSON.stringify(evaluation.config, null, 2)}</pre>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

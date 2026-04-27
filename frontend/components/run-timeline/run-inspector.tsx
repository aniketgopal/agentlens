"use client";

import { useState } from "react";

import { JsonViewer } from "../code-viewer/json-viewer";
import { RunDetail, SecurityFinding, TraceStep } from "../../lib/types";

type StepWithDepth = TraceStep & { depth: number };

export function RunInspector({
  run,
  findings
}: {
  run: RunDetail;
  findings: SecurityFinding[];
}) {
  const [selectedStepId, setSelectedStepId] = useState<string | null>(
    run.steps[0]?.step_id ?? null
  );
  const [activeTab, setActiveTab] = useState<
    "overview" | "input" | "output" | "metadata" | "errors" | "security" | "raw"
  >("overview");

  const selectedStep =
    run.steps.find((step) => step.step_id === selectedStepId) ?? null;
  const orderedSteps = buildOrderedSteps(run.steps);
  const runFindings = findings.filter((finding) => finding.step_id === null);
  const selectedStepFindings = selectedStep
    ? findings.filter((finding) => finding.step_id === selectedStep.step_id)
    : [];
  const findingCountsByStep = new Map<string, number>();
  for (const finding of findings) {
    if (finding.step_id) {
      findingCountsByStep.set(
        finding.step_id,
        (findingCountsByStep.get(finding.step_id) ?? 0) + 1
      );
    }
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="run-summary-grid">
          <div>
            <div className="muted">{run.run_id}</div>
            <h2 style={{ marginBottom: 8 }}>{run.name}</h2>
            <div className={`badge ${run.status}`}>{run.status}</div>
          </div>
          <div className="summary-metric">
            <div className="metric-value">{run.total_tokens}</div>
            <div className="muted">tokens</div>
          </div>
          <div className="summary-metric">
            <div className="metric-value">{run.duration_ms ?? "-"}</div>
            <div className="muted">ms</div>
          </div>
          <div className="summary-metric">
            <div className="metric-value">{run.environment}</div>
            <div className="muted">environment</div>
          </div>
          <div className="summary-metric">
            <div className="metric-value">{run.steps.length}</div>
            <div className="muted">steps</div>
          </div>
          <div className="summary-metric">
            <div className="metric-value">{findings.length}</div>
            <div className="muted">findings</div>
          </div>
        </div>
      </section>

      <section className="inspector-layout">
        <aside className="card inspector-column timeline-column">
          <div className="section-label">Step Timeline</div>
          {run.steps.length === 0 ? (
            <div className="muted">No traced steps for this run yet.</div>
          ) : (
            <div className="timeline-list">
              {orderedSteps.map((step) => {
                const isActive = step.step_id === selectedStepId;
                const stepFindingCount = findingCountsByStep.get(step.step_id) ?? 0;
                return (
                  <button
                    key={step.step_id}
                    type="button"
                    className={`timeline-item${isActive ? " active" : ""}`}
                    onClick={() => {
                      setSelectedStepId(step.step_id);
                      setActiveTab("overview");
                    }}
                    style={{ paddingLeft: 14 + step.depth * 18 }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                      <div>
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                          <div className={`badge ${step.status}`}>{step.status}</div>
                          {stepFindingCount > 0 ? (
                            <div className="badge high">{stepFindingCount} findings</div>
                          ) : null}
                        </div>
                        <div className="timeline-title">{step.name}</div>
                        <div className="muted">{step.type}{step.depth > 0 ? ` · depth ${step.depth}` : ""}</div>
                      </div>
                      <div className="muted">{step.latency_ms ?? "-"} ms</div>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </aside>

        <section className="grid inspector-column">
          <section className="card">
            <div className="section-label">Selected Step</div>
            {selectedStep ? (
              <>
                <div className="tab-row">
                  {[
                    ["overview", "Overview"],
                    ["input", "Input"],
                    ["output", "Output"],
                    ["metadata", "Metadata"],
                    ["errors", "Errors"],
                    ["security", "Security"],
                    ["raw", "Raw JSON"]
                  ].map(([value, label]) => (
                    <button
                      key={value}
                      type="button"
                      className={`tab-button${activeTab === value ? " active" : ""}`}
                      onClick={() =>
                        setActiveTab(
                          value as
                            | "overview"
                            | "input"
                            | "output"
                            | "metadata"
                            | "errors"
                            | "security"
                            | "raw"
                        )
                      }
                    >
                      {label}
                    </button>
                  ))}
                </div>
                <StepPanel
                  step={selectedStep}
                  activeTab={activeTab}
                  findings={selectedStepFindings}
                />
              </>
            ) : (
              <div className="muted">Select a step to inspect its payloads.</div>
            )}
          </section>
        </section>

        <aside className="grid inspector-column">
          <FindingListCard title="Run Findings" findings={runFindings} emptyMessage="No run-level findings." />
          <JsonViewer title="Run Output" value={run.output} />
          <JsonViewer title="Run Input" value={run.input} collapsed />
          <JsonViewer title="Run Metadata" value={run.metadata} collapsed />
        </aside>
      </section>
    </div>
  );
}

function StepSummary({ step }: { step: TraceStep }) {
  return (
    <div className="selected-step-grid">
      <div>
        <div className="muted">Step id</div>
        <div>{step.step_id}</div>
      </div>
      <div>
        <div className="muted">Type</div>
        <div>{step.type}</div>
      </div>
      <div>
        <div className="muted">Status</div>
        <div>{step.status}</div>
      </div>
      <div>
        <div className="muted">Latency</div>
        <div>{step.latency_ms ?? "-"} ms</div>
      </div>
      <div>
        <div className="muted">Started</div>
        <div>{step.started_at}</div>
      </div>
      <div>
        <div className="muted">Ended</div>
        <div>{step.ended_at ?? "-"}</div>
      </div>
      <div>
        <div className="muted">Parent step</div>
        <div>{step.parent_step_id ?? "root"}</div>
      </div>
      <div>
        <div className="muted">Error</div>
        <div>{step.error ? "present" : "none"}</div>
      </div>
    </div>
  );
}

function StepPanel({
  step,
  activeTab,
  findings
}: {
  step: TraceStep;
  activeTab:
    | "overview"
    | "input"
    | "output"
    | "metadata"
    | "errors"
    | "security"
    | "raw";
  findings: SecurityFinding[];
}) {
  if (activeTab === "overview") {
    return <StepSummary step={step} />;
  }

  if (activeTab === "input") {
    return <JsonViewer title="Input" value={step.input} />;
  }

  if (activeTab === "output") {
    return <JsonViewer title="Output" value={step.output} />;
  }

  if (activeTab === "metadata") {
    return (
      <div className="detail-grid">
        <JsonViewer title="Metadata" value={step.metadata} collapsed />
        <JsonViewer title="Model / Usage" value={{ model: step.model, usage: step.usage }} />
      </div>
    );
  }

  if (activeTab === "errors") {
    return (
      <JsonViewer
        title="Errors"
        value={step.error ?? { message: "No error recorded for this step." }}
      />
    );
  }

  if (activeTab === "security") {
    return (
      <FindingListCard
        title="Step Findings"
        findings={findings}
        emptyMessage="No security findings recorded for this step."
      />
    );
  }

  return <JsonViewer title="Raw JSON" value={step} />;
}

function FindingListCard({
  title,
  findings,
  emptyMessage
}: {
  title: string;
  findings: SecurityFinding[];
  emptyMessage: string;
}) {
  return (
    <section className="card">
      <div className="section-label">{title}</div>
      {findings.length === 0 ? (
        <div className="muted">{emptyMessage}</div>
      ) : (
        <div className="finding-list">
          {findings.map((finding) => (
            <div key={finding.finding_id} className="finding-item">
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 8 }}>
                <div className={`badge ${finding.severity}`}>{finding.severity}</div>
                <div className="badge">{finding.category}</div>
              </div>
              <div>{finding.message}</div>
              <div className="muted" style={{ marginTop: 6 }}>
                {finding.rule_id}
              </div>
              <div className="muted">Evidence: {finding.evidence}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function buildOrderedSteps(steps: TraceStep[]): StepWithDepth[] {
  const children = new Map<string | null, TraceStep[]>();
  for (const step of steps) {
    const key = step.parent_step_id ?? null;
    const existing = children.get(key) ?? [];
    existing.push(step);
    children.set(key, existing);
  }

  const ordered: StepWithDepth[] = [];

  function visit(parentId: string | null, depth: number) {
    for (const step of children.get(parentId) ?? []) {
      ordered.push({ ...step, depth });
      visit(step.step_id, depth + 1);
    }
  }

  visit(null, 0);
  return ordered;
}

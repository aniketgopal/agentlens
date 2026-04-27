"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import { SecurityFinding } from "../../lib/types";

const baseUrl =
  process.env.NEXT_PUBLIC_AGENTLENS_API_BASE_URL ?? "http://localhost:8000";

function severityOrder(severity: string): number {
  const ranks: Record<string, number> = {
    critical: 0,
    high: 1,
    medium: 2,
    low: 3,
    info: 4
  };
  return ranks[severity] ?? 5;
}

export function FindingsList({
  initialFindings
}: {
  initialFindings: SecurityFinding[];
}) {
  const [findings, setFindings] = useState(initialFindings);
  const sorted = useMemo(
    () =>
      [...findings].sort(
        (left, right) => severityOrder(left.severity) - severityOrder(right.severity)
      ),
    [findings]
  );

  async function updateFindingStatus(findingId: string, status: SecurityFinding["status"]) {
    const response = await fetch(
      `${baseUrl}/api/v1/security/findings/${encodeURIComponent(findingId)}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
      }
    );
    if (!response.ok) {
      return;
    }
    const payload = await response.json();
    const updated = payload.data as SecurityFinding;
    setFindings((current) =>
      current.map((finding) =>
        finding.finding_id === updated.finding_id ? updated : finding
      )
    );
  }

  return (
    <section className="grid">
      {sorted.map((finding) => (
        <div key={finding.finding_id} className="card">
          <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
            <div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <div className={`badge ${finding.severity}`}>{finding.severity}</div>
                <div className="badge">{finding.status}</div>
              </div>
              <h3 style={{ marginBottom: 8 }}>{finding.category}</h3>
            </div>
            <div className="muted">{finding.created_at}</div>
          </div>
          <p>{finding.message}</p>
          <div className="muted">Rule: {finding.rule_id}</div>
          <div className="muted">Evidence: {finding.evidence}</div>
          <div className="action-row" style={{ marginTop: 14 }}>
            <Link href={`/runs/${finding.run_id}`}>Open run</Link>
            <button
              type="button"
              className="tab-button"
              onClick={() => updateFindingStatus(finding.finding_id, "false_positive")}
            >
              False positive
            </button>
            <button
              type="button"
              className="tab-button"
              onClick={() => updateFindingStatus(finding.finding_id, "resolved")}
            >
              Resolve
            </button>
            <button
              type="button"
              className="tab-button"
              onClick={() => updateFindingStatus(finding.finding_id, "open")}
            >
              Reopen
            </button>
          </div>
        </div>
      ))}
    </section>
  );
}

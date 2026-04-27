"use client";

import Link from "next/link";
import type { Route } from "next";
import { useMemo } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { RunSummary } from "../../lib/types";

export function RunExplorer({
  initialRuns,
  initialStatus = "",
  initialQuery = "",
  initialHasFindings = false
}: {
  initialRuns: RunSummary[];
  initialStatus?: string;
  initialQuery?: string;
  initialHasFindings?: boolean;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const status = searchParams.get("status") ?? initialStatus;
  const query = searchParams.get("q") ?? initialQuery;
  const hasFindings = (searchParams.get("findings") ?? (initialHasFindings ? "1" : "")) === "1";

  function updateParam(name: string, value: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(name, value);
    } else {
      params.delete(name);
    }
    router.push(`${pathname}?${params.toString()}` as Route);
  }

  const filtered = useMemo(() => {
    return initialRuns.filter((run) => {
      if (status && run.status !== status) {
        return false;
      }
      if (hasFindings && run.security_finding_count < 1) {
        return false;
      }
      if (!query) {
        return true;
      }
      const normalized = query.toLowerCase();
      return (
        run.name.toLowerCase().includes(normalized) ||
        run.run_id.toLowerCase().includes(normalized) ||
        run.environment.toLowerCase().includes(normalized)
      );
    });
  }, [hasFindings, initialRuns, query, status]);

  return (
    <div className="grid">
      <section className="card filter-bar">
        <label className="control-group">
          <span className="muted">Search</span>
          <input
            className="control-input"
            value={query}
            onChange={(event) => updateParam("q", event.target.value)}
            placeholder="agent name, run id, environment"
          />
        </label>

        <label className="control-group">
          <span className="muted">Status</span>
          <select
            className="control-input"
            value={status}
            onChange={(event) => updateParam("status", event.target.value)}
          >
            <option value="">All</option>
            <option value="success">Success</option>
            <option value="failed">Failed</option>
            <option value="running">Running</option>
          </select>
        </label>

        <label className="checkbox-row">
          <input
            type="checkbox"
            checked={hasFindings}
            onChange={(event) => updateParam("findings", event.target.checked ? "1" : "")}
          />
          <span>Only runs with findings</span>
        </label>
      </section>

      <section className="card">
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
          <h3 style={{ marginTop: 0 }}>Runs</h3>
          <div className="muted">{filtered.length} visible</div>
        </div>
      </section>

      {filtered.length === 0 ? (
        <section className="card">
          <h3>No runs match the current filters</h3>
          <p className="muted">Clear the filters or run another trace.</p>
        </section>
      ) : (
        <section className="grid runs-grid">
          {filtered.map((run) => (
            <Link key={run.run_id} href={`/runs/${run.run_id}`} className="card">
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <h3 style={{ marginTop: 0 }}>{run.name}</h3>
                <span className={`badge ${run.status}`}>{run.status}</span>
              </div>
              <p className="muted">{run.run_id}</p>
              <p className="muted">Environment: {run.environment}</p>
              <p className="muted">Tokens: {run.total_tokens}</p>
              <p className="muted">Findings: {run.security_finding_count}</p>
            </Link>
          ))}
        </section>
      )}
    </div>
  );
}

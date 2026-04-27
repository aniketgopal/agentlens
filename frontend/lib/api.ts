import {
  EvaluationRecord,
  ProjectSummary,
  RunDetail,
  RunSummary,
  SecurityFinding
} from "./types";

const baseUrl = process.env.NEXT_PUBLIC_AGENTLENS_API_BASE_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  const payload = await response.json();
  return payload.data as T;
}

export function getRuns(projectId: string): Promise<RunSummary[]> {
  return fetchJson<RunSummary[]>(`/api/v1/runs?project_id=${encodeURIComponent(projectId)}`);
}

export function getProjects(): Promise<ProjectSummary[]> {
  return fetchJson<ProjectSummary[]>("/api/v1/projects");
}

export function getRun(runId: string): Promise<RunDetail> {
  return fetchJson<RunDetail>(`/api/v1/runs/${encodeURIComponent(runId)}`);
}

export function getSecurityFindings(projectId: string): Promise<SecurityFinding[]> {
  return fetchJson<SecurityFinding[]>(
    `/api/v1/security/findings?project_id=${encodeURIComponent(projectId)}`
  );
}

export function getRunSecurityFindings(
  projectId: string,
  runId: string
): Promise<SecurityFinding[]> {
  return fetchJson<SecurityFinding[]>(
    `/api/v1/security/findings?project_id=${encodeURIComponent(projectId)}&run_id=${encodeURIComponent(runId)}`
  );
}

export function getEvaluations(projectId: string): Promise<EvaluationRecord[]> {
  return fetchJson<EvaluationRecord[]>(
    `/api/v1/evaluations?project_id=${encodeURIComponent(projectId)}`
  );
}

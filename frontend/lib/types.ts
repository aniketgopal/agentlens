export type RunSummary = {
  run_id: string;
  project_id: string;
  name: string;
  status: string;
  environment: string;
  duration_ms: number | null;
  total_tokens: number;
  total_cost_usd: number;
  error_count: number;
  security_finding_count: number;
  started_at: string;
  ended_at: string | null;
};

export type ProjectSummary = {
  project_id: string;
  name: string;
  description: string | null;
  created_at: string;
};

export type CreatedApiKey = {
  api_key: string;
  key_id: string;
};

export type EvaluationRecord = {
  evaluation_id: string;
  project_id: string;
  run_id: string;
  status: string;
  score: number;
  passed: boolean;
  metrics: Record<string, number>;
  failures: Array<Record<string, string>>;
  config: Record<string, string[]>;
  created_at: string;
};

export type TraceStep = {
  step_id: string;
  id?: string;
  run_id: string;
  project_id: string;
  parent_step_id: string | null;
  type: string;
  name: string;
  status: string;
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  model: Record<string, unknown>;
  usage: Record<string, unknown>;
  latency_ms: number | null;
  started_at: string;
  ended_at: string | null;
  metadata: Record<string, unknown>;
  error: Record<string, unknown> | null;
};

export type SecurityFinding = {
  finding_id: string;
  project_id: string;
  run_id: string;
  step_id: string | null;
  rule_id: string;
  severity: string;
  category: string;
  message: string;
  evidence: string;
  status: string;
  created_at: string;
};

export type RunDetail = RunSummary & {
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  metadata: Record<string, unknown>;
  steps: TraceStep[];
};

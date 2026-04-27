import { EvaluationManager } from "../../components/evaluations/evaluation-manager";
import { ProjectToolbar } from "../../components/layout/project-toolbar";
import { getEvaluations, getProjects, getRuns } from "../../lib/api";
import { resolveSelectedProjectId } from "../../lib/project-selection";
import { EvaluationRecord, ProjectSummary, RunSummary } from "../../lib/types";

export default async function EvaluationsPage({
  searchParams
}: {
  searchParams: Promise<{ project?: string }>;
}) {
  const params = await searchParams;
  let projects: ProjectSummary[] = [];
  let runs: RunSummary[] = [];
  let evaluations: EvaluationRecord[] = [];
  let error: string | null = null;

  try {
    projects = await getProjects();
  } catch (cause) {
    error = cause instanceof Error ? cause.message : "Unknown error";
  }

  const projectId = resolveSelectedProjectId(projects, params.project);

  if (!error && projectId) {
    try {
      runs = await getRuns(projectId);
      evaluations = await getEvaluations(projectId);
    } catch (cause) {
      error = cause instanceof Error ? cause.message : "Unknown error";
    }
  }

  return (
    <div className="grid">
      <ProjectToolbar
        projects={projects}
        currentProjectId={projectId}
        title="Evaluations"
        description="Run simple policy and output checks against traced runs and store the results."
      />

      {error ? (
        <section className="card">
          <h3>Backend unavailable</h3>
          <p className="muted">{error}</p>
        </section>
      ) : !projectId ? (
        <section className="card">
          <h3>No projects yet</h3>
          <p className="muted">Create a project before running evaluations.</p>
        </section>
      ) : runs.length === 0 ? (
        <section className="card">
          <h3>No runs available</h3>
          <p className="muted">Trace at least one run in this project before evaluating it.</p>
        </section>
      ) : (
        <EvaluationManager
          projectId={projectId}
          runs={runs}
          initialEvaluations={evaluations}
        />
      )}
    </div>
  );
}

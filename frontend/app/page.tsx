import { ProjectToolbar } from "../components/layout/project-toolbar";
import { RunExplorer } from "../components/runs/run-explorer";
import { getProjects, getRuns } from "../lib/api";
import { resolveSelectedProjectId } from "../lib/project-selection";
import { ProjectSummary, RunSummary } from "../lib/types";

export default async function HomePage({
  searchParams
}: {
  searchParams: Promise<{
    project?: string;
    status?: string;
    q?: string;
    findings?: string;
  }>;
}) {
  const params = await searchParams;
  let projects: ProjectSummary[] = [];
  let error: string | null = null;

  try {
    projects = await getProjects();
  } catch (cause) {
    error = cause instanceof Error ? cause.message : "Unknown error";
  }

  const projectId = resolveSelectedProjectId(projects, params.project);

  let runs: RunSummary[] = [];
  if (!error && projectId) {
    try {
      runs = await getRuns(projectId);
    } catch (cause) {
      error = cause instanceof Error ? cause.message : "Unknown error";
    }
  }

  return (
    <div className="grid">
      <ProjectToolbar
        projects={projects}
        currentProjectId={projectId}
        title="Run Explorer"
        description="Select a project, search by run id or name, and filter down to the runs that matter."
      />

      {error ? (
        <section className="card">
          <h3>Backend unavailable</h3>
          <p className="muted">{error}</p>
        </section>
      ) : !projectId ? (
        <section className="card">
          <h3>No projects yet</h3>
          <p className="muted">Create your first project from the Projects page, then generate an API key and start tracing runs.</p>
          <p className="muted">For a reproducible demo with seeded runs and security findings:</p>
          <pre>docker compose exec -T backend python /app/scripts/bootstrap_demo.py</pre>
        </section>
      ) : (
        <RunExplorer
          initialRuns={runs}
          initialStatus={params.status ?? ""}
          initialQuery={params.q ?? ""}
          initialHasFindings={params.findings === "1"}
        />
      )}
    </div>
  );
}

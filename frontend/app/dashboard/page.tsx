import Link from "next/link";

import { ProjectToolbar } from "../../components/layout/project-toolbar";
import { getProjects, getRuns } from "../../lib/api";
import { resolveSelectedProjectId } from "../../lib/project-selection";
import { ProjectSummary, RunSummary } from "../../lib/types";

export default async function DashboardPage({
  searchParams
}: {
  searchParams: Promise<{ project?: string }>;
}) {
  const params = await searchParams;
  let projects: ProjectSummary[] = [];
  let runs: RunSummary[] = [];
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
    } catch (cause) {
      error = cause instanceof Error ? cause.message : "Unknown error";
    }
  }

  const totalRuns = runs.length;
  const successRuns = runs.filter((run) => run.status === "success").length;
  const failedRuns = runs.filter((run) => run.status === "failed").length;

  return (
    <div className="grid">
      <ProjectToolbar
        projects={projects}
        currentProjectId={projectId}
        title="Dashboard"
        description="Overview metrics for the selected project. Switch projects without leaving the dashboard."
      />

      {error ? (
        <section className="card">
          <h3>Backend unavailable</h3>
          <p className="muted">{error}</p>
        </section>
      ) : !projectId ? (
        <section className="card">
          <h3>No projects yet</h3>
          <p className="muted">Create a project first. The dashboard will populate once runs exist.</p>
        </section>
      ) : (
        <>
          <section className="grid runs-grid">
            <div className="card">
              <div className="muted">Total runs</div>
              <h3>{totalRuns}</h3>
            </div>
            <div className="card">
              <div className="muted">Successful</div>
              <h3>{successRuns}</h3>
            </div>
            <div className="card">
              <div className="muted">Failed</div>
              <h3>{failedRuns}</h3>
            </div>
          </section>

          <section className="card">
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
              <h3 style={{ marginTop: 0 }}>Recent runs</h3>
              <Link href="/">Open run explorer</Link>
            </div>
            <div className="grid">
              {runs.slice(0, 5).map((run) => (
                <Link key={run.run_id} href={`/runs/${run.run_id}`} className="card">
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <div>{run.name}</div>
                    <span className={`badge ${run.status}`}>{run.status}</span>
                  </div>
                  <div className="muted" style={{ marginTop: 8 }}>
                    {run.run_id}
                  </div>
                </Link>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

import { ProjectToolbar } from "../../components/layout/project-toolbar";
import { getProjects, getSecurityFindings } from "../../lib/api";
import { FindingsList } from "../../components/security/findings-list";
import { resolveSelectedProjectId } from "../../lib/project-selection";
import { ProjectSummary, SecurityFinding } from "../../lib/types";

export default async function SecurityPage({
  searchParams
}: {
  searchParams: Promise<{ project?: string }>;
}) {
  const params = await searchParams;
  let projects: ProjectSummary[] = [];
  let findings: SecurityFinding[] = [];
  let error: string | null = null;

  try {
    projects = await getProjects();
  } catch (cause) {
    error = cause instanceof Error ? cause.message : "Unknown error";
  }

  const projectId = resolveSelectedProjectId(projects, params.project);

  if (!error && projectId) {
    try {
      findings = await getSecurityFindings(projectId);
    } catch (cause) {
      error = cause instanceof Error ? cause.message : "Unknown error";
    }
  }

  return (
    <div className="grid">
      <ProjectToolbar
        projects={projects}
        currentProjectId={projectId}
        title="Security Findings"
        description="Findings are generated from step payloads and final run output using the MVP rule scanner."
      />

      {error ? (
        <section className="card">
          <h3>Backend unavailable</h3>
          <p className="muted">{error}</p>
        </section>
      ) : !projectId ? (
        <section className="card">
          <h3>No projects yet</h3>
          <p className="muted">Create a project and start tracing runs to generate security findings.</p>
        </section>
      ) : findings.length === 0 ? (
        <section className="card">
          <h3>No findings yet</h3>
          <p className="muted">Run a trace that contains prompt injection or sensitive-data patterns.</p>
        </section>
      ) : (
        <FindingsList initialFindings={findings} />
      )}
    </div>
  );
}

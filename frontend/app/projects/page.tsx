import { ProjectManager } from "../../components/projects/project-manager";
import { getProjects } from "../../lib/api";
import { ProjectSummary } from "../../lib/types";

export default async function ProjectsPage() {
  let projects: ProjectSummary[] = [];
  let error: string | null = null;

  try {
    projects = await getProjects();
  } catch (cause) {
    error = cause instanceof Error ? cause.message : "Unknown error";
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="section-label">Projects</div>
        <h2 style={{ marginTop: 12 }}>Project and API key management</h2>
        <p className="muted">
          Create projects and generate ingestion keys without leaving the product.
        </p>
      </section>

      {error ? (
        <section className="card">
          <h3>Backend unavailable</h3>
          <p className="muted">{error}</p>
        </section>
      ) : (
        <ProjectManager initialProjects={projects} />
      )}
    </div>
  );
}

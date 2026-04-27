"use client";

import { useMemo, useState } from "react";

import { CreatedApiKey, ProjectSummary } from "../../lib/types";

const baseUrl =
  process.env.NEXT_PUBLIC_AGENTLENS_API_BASE_URL ?? "http://localhost:8000";

export function ProjectManager({
  initialProjects
}: {
  initialProjects: ProjectSummary[];
}) {
  const [projects, setProjects] = useState(initialProjects);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [latestKey, setLatestKey] = useState<{
    projectId: string;
    projectName: string;
    value: CreatedApiKey;
  } | null>(null);
  const [busyProjectId, setBusyProjectId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const orderedProjects = useMemo(
    () => [...projects].sort((left, right) => left.name.localeCompare(right.name)),
    [projects]
  );

  async function createProject() {
    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }
    setError(null);
    setIsCreating(true);
    try {
      const response = await fetch(`${baseUrl}/api/v1/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          description: description.trim() || null
        })
      });
      if (!response.ok) {
        throw new Error(`Project creation failed: ${response.status}`);
      }
      const payload = await response.json();
      setProjects((current) => [payload.data as ProjectSummary, ...current]);
      setName("");
      setDescription("");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unknown error");
    } finally {
      setIsCreating(false);
    }
  }

  async function createApiKey(project: ProjectSummary) {
    setError(null);
    setBusyProjectId(project.project_id);
    try {
      const response = await fetch(
        `${baseUrl}/api/v1/projects/${encodeURIComponent(project.project_id)}/api-keys`,
        {
          method: "POST"
        }
      );
      if (!response.ok) {
        throw new Error(`API key creation failed: ${response.status}`);
      }
      const payload = await response.json();
      setLatestKey({
        projectId: project.project_id,
        projectName: project.name,
        value: payload.data as CreatedApiKey
      });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unknown error");
    } finally {
      setBusyProjectId(null);
    }
  }

  async function copyLatestKey() {
    if (!latestKey) {
      return;
    }
    await navigator.clipboard.writeText(latestKey.value.api_key);
  }

  return (
    <div className="grid">
      <section className="card">
        <div className="section-label">Create Project</div>
        <div className="project-form">
          <label className="control-group">
            <span className="muted">Name</span>
            <input
              className="control-input"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Recruiting Agent"
            />
          </label>
          <label className="control-group">
            <span className="muted">Description</span>
            <input
              className="control-input"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Candidate screening workflow"
            />
          </label>
          <button
            type="button"
            className="tab-button"
            onClick={createProject}
            disabled={isCreating}
          >
            {isCreating ? "Creating..." : "Create project"}
          </button>
        </div>
        {error ? <p className="muted" style={{ marginTop: 12 }}>{error}</p> : null}
      </section>

      {latestKey ? (
        <section className="card">
          <div className="section-label">Latest API Key</div>
          <h3 style={{ marginTop: 0 }}>{latestKey.projectName}</h3>
          <p className="muted">This value is only shown once. Store it now.</p>
          <pre>{latestKey.value.api_key}</pre>
          <div className="action-row" style={{ marginTop: 12 }}>
            <button type="button" className="tab-button" onClick={copyLatestKey}>
              Copy key
            </button>
            <span className="muted">{latestKey.value.key_id}</span>
          </div>
        </section>
      ) : null}

      <section className="grid runs-grid">
        {orderedProjects.map((project) => (
          <div key={project.project_id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
              <div>
                <h3 style={{ marginTop: 0, marginBottom: 8 }}>{project.name}</h3>
                <div className="muted">{project.project_id}</div>
              </div>
              <button
                type="button"
                className="tab-button"
                onClick={() => createApiKey(project)}
                disabled={busyProjectId === project.project_id}
              >
                {busyProjectId === project.project_id ? "Generating..." : "Generate API key"}
              </button>
            </div>
            <p className="muted" style={{ marginTop: 12 }}>
              {project.description || "No description"}
            </p>
            <div className="muted">Created: {project.created_at}</div>
          </div>
        ))}
      </section>
    </div>
  );
}

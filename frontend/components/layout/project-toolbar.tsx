"use client";

import type { Route } from "next";
import { useRouter, useSearchParams, usePathname } from "next/navigation";

import { ProjectSummary } from "../../lib/types";

export function ProjectToolbar({
  projects,
  currentProjectId,
  title,
  description
}: {
  projects: ProjectSummary[];
  currentProjectId: string | null;
  title: string;
  description: string;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  function updateParam(name: string, value: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(name, value);
    } else {
      params.delete(name);
    }
    router.push(`${pathname}?${params.toString()}` as Route);
  }

  return (
    <section className="card toolbar-card">
      <div>
        <div className="section-label">{title}</div>
        <h2 style={{ marginTop: 12, marginBottom: 8 }}>{currentProjectId ?? "No project selected"}</h2>
        <p className="muted">{description}</p>
      </div>
      <div className="toolbar-controls">
        {projects.length > 0 ? (
          <label className="control-group">
            <span className="muted">Project</span>
            <select
              className="control-input"
              value={currentProjectId ?? ""}
              onChange={(event) => updateParam("project", event.target.value)}
            >
              {projects.map((project) => (
                <option key={project.project_id} value={project.project_id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
        ) : null}
      </div>
    </section>
  );
}

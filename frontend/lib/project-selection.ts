import { ProjectSummary } from "./types";

export function resolveSelectedProjectId(
  projects: ProjectSummary[],
  requestedProjectId?: string
): string | null {
  if (requestedProjectId && projects.some((project) => project.project_id === requestedProjectId)) {
    return requestedProjectId;
  }
  return projects[0]?.project_id ?? null;
}

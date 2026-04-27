import { getRun, getRunSecurityFindings } from "../../../lib/api";
import { RunInspector } from "../../../components/run-timeline/run-inspector";

export default async function RunDetailPage({
  params
}: {
  params: Promise<{ runId: string }>;
}) {
  const { runId } = await params;
  const run = await getRun(runId);
  const findings = await getRunSecurityFindings(run.project_id, runId);

  return <RunInspector run={run} findings={findings} />;
}

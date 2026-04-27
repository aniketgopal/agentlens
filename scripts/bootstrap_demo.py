from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib import error, request


ROOT = Path(__file__).resolve().parent.parent
API_BASE_URL = os.environ.get("AGENTLENS_API_BASE_URL", "http://127.0.0.1:8000")
DASHBOARD_URL = os.environ.get("AGENTLENS_DASHBOARD_URL", "http://localhost:3000")
TRACE_ENDPOINT = os.environ.get("AGENTLENS_ENDPOINT", API_BASE_URL)


def post_json(path: str, payload: dict[str, object] | None = None) -> dict[str, object]:
    url = f"{API_BASE_URL}{path}"
    raw = json.dumps(payload or {}).encode("utf-8")
    req = request.Request(
        url,
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Request failed: {exc.code} {url}\n{body}") from exc


def run_example(script: Path, project_id: str, api_key: str) -> None:
    env = os.environ.copy()
    env["AGENTLENS_API_KEY"] = api_key
    env["AGENTLENS_PROJECT_ID"] = project_id
    env["AGENTLENS_ENDPOINT"] = TRACE_ENDPOINT
    env["PYTHONPATH"] = str(ROOT / "sdk" / "python")
    subprocess.run([sys.executable, str(script)], check=True, env=env, cwd=str(ROOT))


def main() -> None:
    project_payload = {
        "name": "AgentLens Demo Project",
        "description": "Seeded onboarding demo with standard and security traces.",
    }
    project_response = post_json("/api/v1/projects", project_payload)
    project = project_response["data"]
    project_id = str(project["project_id"])

    key_response = post_json(f"/api/v1/projects/{project_id}/api-keys")
    api_key = str(key_response["data"]["api_key"])

    print(f"Created project: {project_id}")
    print("Running simple-agent demo...")
    run_example(ROOT / "examples" / "simple-agent" / "main.py", project_id, api_key)

    print("Running security demo...")
    run_example(ROOT / "examples" / "security-demo" / "main.py", project_id, api_key)

    print("\nDemo ready:")
    print(f"Project ID: {project_id}")
    print(f"API Key: {api_key}")
    print(f"Runs: {DASHBOARD_URL}/?project={project_id}")
    print(f"Security: {DASHBOARD_URL}/security?project={project_id}")
    print(f"Projects: {DASHBOARD_URL}/projects")


if __name__ == "__main__":
    main()

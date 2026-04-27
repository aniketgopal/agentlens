"use client";

import { useState } from "react";

export function JsonViewer({
  title,
  value,
  collapsed = false
}: {
  title: string;
  value: unknown;
  collapsed?: boolean;
}) {
  const [isCollapsed, setIsCollapsed] = useState(collapsed);
  const pretty = JSON.stringify(value, null, 2);

  async function copyJson() {
    await navigator.clipboard.writeText(pretty);
  }

  return (
    <section className="card">
      <div className="json-header">
        <div className="section-label" style={{ marginBottom: 0 }}>
          {title}
        </div>
        <div className="json-actions">
          <button
            type="button"
            className="tab-button"
            onClick={() => setIsCollapsed((current) => !current)}
          >
            {isCollapsed ? "Expand" : "Collapse"}
          </button>
          <button type="button" className="tab-button" onClick={copyJson}>
            Copy
          </button>
        </div>
      </div>
      {isCollapsed ? (
        <pre>{pretty.slice(0, 160)}{pretty.length > 160 ? "..." : ""}</pre>
      ) : (
        <pre>{pretty}</pre>
      )}
    </section>
  );
}

import Link from "next/link";
import type { Route } from "next";

const navItems = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Runs", href: "/" },
  { label: "Evaluations", href: "/evaluations" },
  { label: "Security", href: "/security" },
  { label: "Projects", href: "/projects" },
  { label: "Settings", href: "/settings" }
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div style={{ marginBottom: 28 }}>
        <div className="muted" style={{ fontSize: 12, letterSpacing: 1.4, textTransform: "uppercase" }}>
          Agent Reliability
        </div>
        <h1 style={{ margin: "8px 0 0", fontSize: 28 }}>AgentLens</h1>
      </div>
      <nav className="grid">
        {navItems.map((item) => (
          <Link
            key={item.label}
            href={item.href as Route}
            className="card"
            style={{ padding: "14px 16px" }}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}

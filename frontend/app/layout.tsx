import "./globals.css";
import { ReactNode } from "react";

import { Sidebar } from "../components/layout/sidebar";

export const metadata = {
  title: "AgentLens",
  description: "AI agent reliability dashboard"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <Sidebar />
          <main className="content">{children}</main>
        </div>
      </body>
    </html>
  );
}

"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Page() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="vantageai">
      <main style={{ display: "flex", height: "100vh" }}>
        <section style={{ flex: 1, padding: 24, overflow: "auto" }}>
          <h1>VantageAI</h1>
          <p>Describe a business idea and the agent will build your dashboard here.</p>
          {/* A2UI panels mount here as the agent emits UI specs. */}
        </section>
        <aside style={{ width: 420, borderLeft: "1px solid #eee" }}>
          <CopilotChat
            labels={{
              title: "VantageAI",
              initial: 'Try: "I want to open a Pilates studio in Shoreditch."',
            }}
          />
        </aside>
      </main>
    </CopilotKit>
  );
}

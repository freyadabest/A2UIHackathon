# VantageAI — Architecture (MVP)

```mermaid
flowchart TB
    user([User: "Open a Pilates studio in Shoreditch"])

    subgraph Browser["Browser — Next.js + CopilotKit"]
        chat["CopilotChat"]
        canvas["A2UI Canvas<br/>CompetitorTable mounts here"]
    end

    runtime["CopilotKit Copilot Runtime<br/>/api/copilotkit"]

    subgraph Agent["Agent — Python (FastAPI + Gemini)"]
        orch["Orchestrator (Gemini)"]
        tool["discover_competitors"]
        ui["ui_specs → A2UI panel spec"]
    end

    redis[("Redis<br/>cache · state")]
    linkup{{"Linkup API<br/>Search"}}

    user --> chat
    chat -- "AG-UI" --> runtime
    runtime -- "AG-UI" --> orch
    orch --> tool --> linkup
    tool --> ui
    ui -- "AG-UI: UI spec" --> canvas
    tool <--> redis
```

## Flow

1. User sends one sentence into **CopilotChat**.
2. **Copilot Runtime** forwards it to the Python agent over **AG-UI**.
3. The orchestrator calls **`discover_competitors`**, which queries **Linkup** (cached via **Redis**).
4. The result becomes an **A2UI panel spec** emitted back over AG-UI.
5. CopilotKit mounts **`CompetitorTable`** with the data — the panel renders live.

See [`README.md`](../README.md) for stack and quickstart.

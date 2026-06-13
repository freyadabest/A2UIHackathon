# VantageAI — Architecture

```mermaid
flowchart TB
    user([User: "Open a Pilates studio in Shoreditch"])

    subgraph Browser["Browser — Next.js + CopilotKit"]
        chat["CopilotChat<br/>(single prompt entry)"]
        canvas["A2UI Canvas<br/>panels mount as agent emits UI specs"]
    end

    runtime["CopilotKit Copilot Runtime<br/>/api/copilotkit"]

    subgraph Agent["Agent service — Python (ADK / FastAPI + Gemini)"]
        orch["Orchestrator (Gemini)"]
        t1["discover_competitors"]
        t2["get_reviews_sentiment"]
        t3["get_financial_signals"]
        t4["get_area_demographics"]
        t5["score_opportunity"]
        ui["ui_specs → A2UI panel specs"]
    end

    redis[("Redis<br/>cache · state · vectors · pub/sub")]
    linkup{{"Linkup API<br/>Search / Research"}}
    gemini{{"Gemini"}}
    places{{"Google Places<br/>(optional)"}}

    user --> chat
    chat -- "AG-UI" --> runtime
    runtime -- "AG-UI" --> orch
    orch --> t1 & t2 & t3 & t4 & t5
    t1 & t2 & t3 & t4 --> linkup
    t2 & t5 --> gemini
    t1 -.-> places
    t1 & t2 & t3 & t4 & t5 --> ui
    ui -- "AG-UI: UI spec" --> canvas
    Agent <--> redis
```

## Flow

1. User sends one sentence into **CopilotChat**.
2. **Copilot Runtime** forwards it to the Python agent over **AG-UI**.
3. The **orchestrator** (Gemini) plans and calls tools. Each tool hits **Linkup** (and optionally Google Places / Gemini), cached through **Redis**.
4. On completion, each tool produces an **A2UI panel spec** emitted back over AG-UI.
5. CopilotKit's **A2UI renderer** mounts the matching React panel, populated with the data — the dashboard assembles itself live.
6. **Redis** holds the evolving dashboard state so follow-up questions ("which competitor is weakest?") can read/update panels.

See the top-level [`README.md`](../README.md) for the full stack and build phases.

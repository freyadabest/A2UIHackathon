# VantageAI — Architecture (MVP)

Two views: the **component architecture** (what runs where) and the **user flow** (what happens when someone asks a question).

---

## 1. Component architecture

```mermaid
flowchart LR
    subgraph Browser["Browser"]
        direction TB
        chat["CopilotChat<br/>(prompt input)"]
        canvas["A2UI Canvas"]
        panel["CompetitorTable<br/>(registerPanels.ts)"]
        canvas --> panel
    end

    subgraph Web["apps/web — Next.js"]
        route["/api/copilotkit<br/>Copilot Runtime"]
    end

    subgraph AgentSvc["services/agent — Python (FastAPI)"]
        direction TB
        server["AG-UI server<br/>main.py"]
        orch["Orchestrator (Gemini)<br/>agent.py"]
        tool["discover_competitors<br/>tools/competitors.py"]
        client["linkup_client.py"]
        specs["ui_specs.py"]
        server --> orch --> tool --> client
        tool --> specs
    end

    redis[("Redis<br/>cache · state")]
    linkup{{"Linkup API"}}
    gemini{{"Gemini API"}}

    chat -->|AG-UI| route
    route -->|AG-UI| server
    specs -->|AG-UI: UI spec| canvas
    orch -.-> gemini
    client --> linkup
    client <--> redis
```

**Pieces**
- **Browser** — `CopilotChat` for input; the **A2UI canvas** mounts React panels (`CompetitorTable`) by name via `lib/registerPanels.ts`.
- **apps/web** — Next.js app; `/api/copilotkit` runs the **Copilot Runtime**, which bridges the browser to the agent over **AG-UI**.
- **services/agent** — Python FastAPI **AG-UI server**; the Gemini **orchestrator** calls the `discover_competitors` tool, which uses `linkup_client` (Redis-cached) and builds an A2UI panel spec via `ui_specs`.
- **External** — **Linkup** (web search), **Gemini** (reasoning), **Redis** (cache + shared state).

---

## 2. User flow

```mermaid
sequenceDiagram
    actor U as User
    participant C as CopilotChat
    participant R as Copilot Runtime<br/>(/api/copilotkit)
    participant A as Agent (Gemini)
    participant L as Linkup API
    participant D as Redis
    participant P as A2UI Canvas

    U->>C: "Open a Pilates studio in Shoreditch"
    C->>R: prompt (AG-UI)
    R->>A: forward (AG-UI)
    A->>A: parse business_type + area
    A->>D: check cache
    alt cache miss
        A->>L: search competitors (structured)
        L-->>A: competitor list
        A->>D: store in cache
    else cache hit
        D-->>A: cached competitor list
    end
    A->>A: build CompetitorTable spec (ui_specs)
    A-->>R: UI spec (AG-UI)
    R-->>P: mount CompetitorTable
    P-->>U: live competitor table
```

**Flow**
1. User types one sentence into **CopilotChat**.
2. The **Copilot Runtime** forwards it to the agent over **AG-UI**.
3. The agent extracts `business_type` + `area`, checks **Redis**, and on a miss queries **Linkup** for competitors (caching the result).
4. The agent builds a **`CompetitorTable`** A2UI spec and emits it back over AG-UI.
5. The **A2UI canvas** mounts the panel with the data — the user sees a live competitor table.

See [`README.md`](../README.md) for stack and quickstart.

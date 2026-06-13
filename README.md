# VantageAI

**Describe a business idea, and watch an AI agent build you a live market-intelligence dashboard from real data.**

> Demo: *"I want to open a Pilates studio in Shoreditch. Who's already there, how are they doing, and is there room for me?"*

VantageAI takes a single sentence, fans out across real web data, and **generatively assembles a multi-panel intelligence dashboard** — competitor mapping, review sentiment, operational patterns, financial health, customer demographics, and a "is there room for me?" opportunity verdict — panel by panel, as each analysis completes.

Built for the **A2UI Hackathon** (Freya & Rosemary).

---

## Stack

| Tech | Role |
|---|---|
| **CopilotKit** | Product UX layer — chat entry point, Copilot Runtime, generative-UI rendering |
| **AG-UI** | Agent↔UI protocol (event stream: messages, tool calls, state, UI) |
| **A2UI** | Declarative generative UI — the agent emits UI specs, the frontend mounts real React panels |
| **Linkup API** | Live web intelligence: competitor discovery, reviews/sentiment, news, financial & market signals (with citations) |
| **Redis** | Response cache, shared agent state, vector cache for sentiment, pub/sub streaming, rate-limit |
| **Gemini (Google)** | Reasoning model behind the agent |

> **Note:** Linkup is the primary intelligence engine (web search/answer/research). Google Places (New) is an optional add-on for precise map pins + structured ratings.

---

## Quickstart

```bash
cp .env.example .env   # fill in LINKUP_API_KEY, GOOGLE_API_KEY
docker compose up      # web :3000 · agent :8000 · redis :6379

# or run pieces locally:
cd services/agent && pip install -r requirements.txt && uvicorn main:app --reload
cd apps/web && npm install && npm run dev
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the architecture diagram.

---

## How it works

```
Browser (Next.js + CopilotKit)
  │  CopilotChat — single prompt entry
  │  A2UI canvas — panels mount as the agent emits UI specs
  ▼  AG-UI event stream
CopilotKit Copilot Runtime  (/api/copilotkit)
  ▼  AG-UI
Agent service (Python — Google ADK or FastAPI + Gemini)
  Orchestrator (Gemini) → tools:
    • discover_competitors    → Linkup Search (structured output)
    • get_reviews_sentiment   → Linkup Search + Gemini
    • get_financial_signals   → Linkup Research (deep, cited)
    • get_area_demographics   → Linkup Search (+ ONS optional)
    • get_competitor_geo      → Google Places (optional)
    • score_opportunity       → Gemini synthesis
  each tool → emits an A2UI panel spec back over AG-UI
  ▼  cache · state · vectors
Redis
```

**Core loop:** one sentence in → orchestrator plans → each tool runs (Linkup, cached via Redis) → on completion the agent emits a **UI spec** over AG-UI → CopilotKit's A2UI renderer mounts the matching React panel, populated with that data. The dashboard builds itself live.

---

## Dashboard panels

| Panel | Tool | Data |
|---|---|---|
| **CompetitorTable** | `discover_competitors` | name, rating, location, URL (Linkup structured output) |
| **CompetitorMap** | `get_competitor_geo` *(optional)* | map pins (Google Places) |
| **SentimentBoard** | `get_reviews_sentiment` | per-competitor sentiment + praise/complaint themes |
| **OperationalPanel** | `discover_competitors` | hours / class types |
| **FinancialHealthCards** | `get_financial_signals` | company age, funding, news, fragility signals + citations |
| **DemographicsPanel** | `get_area_demographics` | area population / income / age profile |
| **OpportunityVerdict** *(hero)* | `score_opportunity` | white-space score + plain-English verdict |

---

## Repo layout (planned)

```
vantageai/
├─ apps/web/                      # Next.js + CopilotKit frontend
│  ├─ app/page.tsx                # dashboard canvas + CopilotChat
│  ├─ app/api/copilotkit/route.ts # Copilot Runtime endpoint
│  ├─ components/panels/          # A2UI panels
│  └─ lib/registerPanels.ts       # maps panel name → component (A2UI)
├─ services/agent/                # Python agent (ADK or FastAPI + Gemini)
│  ├─ main.py                     # AG-UI server entrypoint
│  ├─ agent.py                    # orchestrator + sub-agents
│  ├─ tools/                      # linkup_client, competitors, sentiment, ...
│  ├─ cache.py                    # Redis: cache, shared state, vectors
│  └─ ui_specs.py                 # builds A2UI panel specs
├─ .env
└─ docker-compose.yml             # web + agent + redis
```

---

## Redis usage

1. **Response cache** — hash(query+params) → cached Linkup/Places responses with TTL (speed + demo safety).
2. **Shared agent state** — evolving dashboard state for follow-up questions.
3. **Vector cache** — review embeddings (RediSearch) for dedup + theme clustering.
4. **Pub/Sub** — stream tool progress to the UI.
5. **Rate-limit / dedupe** — protect Linkup quota.

---

## Build phases

- **Phase 0 — Scaffold:** Next.js + CopilotKit, `/api/copilotkit` → agent over AG-UI, `docker-compose up` (web + agent + Redis). *Milestone: agent renders one panel.*
- **Phase 1 — Competitor discovery (MVP):** Linkup `discover_competitors` → live `CompetitorTable`.
- **Phase 2 — Sentiment:** Linkup + Gemini → `SentimentBoard` (Redis vector cache).
- **Phase 3 — Verdict:** `score_opportunity` → `OpportunityVerdict`.
- **Phase 4 — Stretch:** `FinancialHealthCards` (Linkup Research), `DemographicsPanel`, `CompetitorMap`, conversational drill-down.
- **Phase 5 — Demo hardening:** pre-warm Redis cache, `DEMO_MODE` replay, rehearse.

---

## Environment

```
LINKUP_API_KEY=          # app.linkup.so — API key (free credits)
GOOGLE_API_KEY=          # Gemini (AI Studio)
GOOGLE_MAPS_API_KEY=     # optional: Places + Maps JS
REDIS_URL=redis://redis:6379
```

- Linkup: `pip install linkup-sdk` / `npm i linkup-sdk`. `Search` with `outputType` (`searchResults` | `sourcedAnswer` | `structured`) + `depth`; `Research` for deep cited reports.
- Redis: use the `redis-stack` image for vector search.

---

## Status

Planning + scaffolding stage. See build phases above.

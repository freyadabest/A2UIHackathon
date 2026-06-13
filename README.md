# VantageAI

**Describe a business idea, and watch an AI agent build you a live competitor dashboard from real web data.**

> Demo: *"I want to open a Pilates studio in Shoreditch. Who's already there?"*

Built for the **A2UI Hackathon** (Freya & Rosemary).

---

## What the MVP does

One sentence in → the agent **parses** the idea into a business type + area,
**discovers competitors** via live **Linkup** web search, computes market signals,
and **generatively renders** a dashboard of panels (A2UI): a market summary, a
ratings chart, and a competitor table.

It runs with **zero secrets** — without `LINKUP_API_KEY` it serves sample data,
and without `GOOGLE_API_KEY` it parses ideas with a heuristic. Add the keys for
live results.

## Stack

| Tech | Role |
|---|---|
| **Next.js + A2UI panel registry** | Generative, agent-rendered React panels |
| **FastAPI agent** | Idea parsing → tools → A2UI panel specs |
| **Linkup API** | Live web search for competitor discovery |
| **Gemini** *(optional)* | Idea parsing (heuristic fallback if absent) |
| **Redis** *(optional)* | Response cache (no-op if absent) |

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the diagram.

---

## Quickstart

```bash
cp .env.example .env   # optional: add LINKUP_API_KEY (+ GOOGLE_API_KEY)
./run.sh               # starts agent :8000 and web :3000
```

Then open http://localhost:3000 and type an idea (or click an example).

<details>
<summary>Run the pieces individually</summary>

```bash
# Agent (FastAPI) on :8000
cd services/agent && python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt && uvicorn main:app --reload

# Web (Next.js) on :3000
cd apps/web && npm install && npm run dev
```

Or `docker compose up` (web :3000 · agent :8000 · redis :6379).
</details>

### Agent API

```
GET  /health        # liveness + which keys are active
POST /dashboard     # { "idea": "..." } -> { panels: [...] }  (the demo path)
POST /competitors   # { "business_type": "...", "area": "..." }
```

## Structure

```
apps/web/                  # Next.js (A2UI generative UI)
  app/page.tsx             # idea prompt + dashboard canvas
  app/api/dashboard/       # proxy → agent /dashboard
  components/PanelRenderer.tsx   # panel spec -> registered component
  components/panels/       # MarketSummary, RatingsChart, CompetitorTable
  lib/registerPanels.ts    # panel name → React component
services/agent/            # Python FastAPI
  main.py                  # /health + /dashboard + /competitors
  agent.py                 # orchestrator (parse_idea → discover → build panels)
  tools/                   # idea_parser, linkup_client, competitors
  ui_specs.py              # A2UI panel spec builders
  cache.py                 # optional Redis cache
run.sh · docker-compose.yml
```

## Status

Runnable, demoable MVP: `idea → parse → discover_competitors → {MarketSummary,
RatingsChart, CompetitorTable}` is wired end-to-end.

# VantageAI

**Describe a business idea, and watch an AI agent build you a live competitor dashboard from real web data.**

> Demo: *"I want to open a Pilates studio in Shoreditch. Who's already there?"*

Built for the **A2UI Hackathon** (Freya & Rosemary).

---

## MVP scope

One sentence in → the agent discovers local competitors via **Linkup** and **generatively renders a competitor table** in the UI (A2UI). That's the demoable core; everything else is additive later.

## Stack

| Tech | Role |
|---|---|
| **CopilotKit + AG-UI + A2UI** | Chat entry point + agent-rendered React panels |
| **Linkup API** | Live web search for competitor discovery |
| **Redis** | Response cache + shared state |
| **Gemini** | Reasoning model behind the agent |

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the diagram.

---

## Quickstart

```bash
cp .env.example .env   # fill in LINKUP_API_KEY, GOOGLE_API_KEY
docker compose up      # web :3000 · agent :8000 · redis :6379

# or run locally:
cd services/agent && pip install -r requirements.txt && uvicorn main:app --reload
cd apps/web && npm install && npm run dev
```

## Structure

```
apps/web/                  # Next.js + CopilotKit
  app/page.tsx             # CopilotChat + A2UI canvas
  app/api/copilotkit/      # Copilot Runtime → agent
  components/panels/       # CompetitorTable
  lib/registerPanels.ts    # panel name → React component
services/agent/            # Python FastAPI + AG-UI
  main.py                  # /health + /competitors
  agent.py                 # orchestrator + tools
  tools/                   # linkup_client, competitors
  cache.py                 # Redis
  ui_specs.py              # A2UI panel specs
docker-compose.yml
```

## Status

MVP scaffold. The `discover_competitors → CompetitorTable` path is wired as the starting point.

---
name: testing-vantage-ai
description: Test the Vantage AI market scan feature end-to-end. Use when verifying changes to the competitive-intelligence dashboard, research_market tool, or fixed_agent.
---

# Testing Vantage AI

## Devin Secrets Needed

- `GEMINI_API_KEY` — Gemini API key (powers the LangGraph agent). Get at https://aistudio.google.com/apikey
- `LINKUP_API_KEY` — Linkup web-search API key (competitor discovery). Get at https://app.linkup.so

## Local Setup

1. Install dependencies:
   ```bash
   cd /home/ubuntu/repos/A2UIHackathon && pnpm install --frozen-lockfile
   ```
   This also runs `postinstall` which sets up the Python agent venv via `uv`.

2. Create `.env` at repo root:
   ```bash
   echo "GEMINI_API_KEY=${GEMINI_API_KEY}" > .env
   echo "LINKUP_API_KEY=${LINKUP_API_KEY}" >> .env
   echo "FIXED_AGENT_URL=http://localhost:8123/fixed" >> .env
   echo "DYNAMIC_AGENT_URL=http://localhost:8123/dynamic" >> .env
   ```

3. Start the agent (FastAPI on port 8123):
   ```bash
   cd agent && GEMINI_API_KEY=${GEMINI_API_KEY} LINKUP_API_KEY=${LINKUP_API_KEY} uv run uvicorn main:app --port 8123 --reload
   ```

4. Start the frontend (Next.js on port 3000):
   ```bash
   cd /home/ubuntu/repos/A2UIHackathon && pnpm dev:ui
   ```

## Primary Test Flow: Market Scan

1. Navigate to `http://localhost:3000` — verify Vantage AI branding (logo, "sign the lease" hero, A2UI v0.9 eyebrow)
2. Click "Run a market scan" card → navigates to `/fixed`
3. Verify split view: chat panel (left) with placeholder "Describe an area + business…", empty canvas (right) with hint "TRY: PILATES STUDIO IN SHOREDITCH"
4. Type "I want to open a Pilates studio in Shoreditch" and submit
5. Wait ~10-15s for agent to call `research_market` then `render_dashboard`
6. Verify dashboard renders on canvas with:
   - Header with eyebrow containing "SHOREDITCH" and "PILATES"
   - 4 KPI stat cards (competitors, avg rating, avg price, opportunity score)
   - Line chart (demand curve)
   - Donut chart (service mix)
   - Data table with competitor rows (columns: Studio, Area, Rating/price, Δ)
   - Scope chips (e.g. Shoreditch, Hoxton, Spitalfields, By rating)
7. Click a scope chip (e.g. "Hoxton") — dashboard should re-render with new data for that area

## Key Assertions

- Dashboard has **exactly 4 KPI cards**
- Competitor names come from Linkup (real businesses, not hallucinated)
- Scope chip click triggers new `research_market` call and updates all dashboard sections
- If LINKUP_API_KEY is missing, agent returns gracefully with status "error" and a note (not a crash)

## Offline Mode

Set `OFFLINE=1` env var to test without Gemini. This uses a deterministic stub that renders a canned Shoreditch dashboard. Useful for testing UI rendering without API costs.

## Architecture Notes

- Frontend route: `src/app/(pdf)/fixed/page.tsx` — uses CopilotChat with `agentId="fixed_agent"`
- API route: `src/app/api/copilotkit-pdf/route.ts` — proxies to agent at localhost:8123/fixed
- Agent: `agent/src/fixed_agent.py` — LangGraph ReAct agent with `research_market` + `render_dashboard` tools
- Research tool: `agent/src/research_tools.py` — Linkup SDK structured search
- Dashboard schema: `agent/src/a2ui/schemas/dashboard.json` — A2UI v0.9 declarative layout

## Troubleshooting

- If the canvas stays empty after submitting, check agent logs for Gemini API errors (rate limits, invalid key)
- If competitor data shows status "empty", the Linkup key might be expired or the query too niche
- The `pnpm doctor` script checks for common env issues before boot
- Port 8123 must be free for the agent; port 3000 for the frontend

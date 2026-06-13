# Vantage AI — Competitive-Landscape Intelligence

**Vantage AI** is a live competitive-intelligence dashboard powered by [Linkup](https://www.linkup.so/) web search and rendered with **A2UI v0.9** generative UI. Type an area + business type (e.g. *"Pilates studio in Shoreditch"*) and get a real-time dashboard with KPIs, charts, competitor tables, and interactive scope chips — all driven by an autonomous agent.

Built on the [CopilotKit](https://copilotkit.ai) × [A2UI](https://a2ui.org/) starter for the **London A2A & A2UI Hackathon** (Google London CSG, June 13 2026).

---

## How it works

1. You describe an area + business in chat
2. The **LangGraph agent** (Gemini 3.5 Flash) calls `research_market` → [Linkup API](https://www.linkup.so/) for live competitor data
3. The agent calls `render_dashboard` → emits an A2UI envelope with KPIs, charts, and tables
4. **CopilotKit** streams the envelope to the Next.js frontend, which renders it as a live React dashboard
5. Click a **scope chip** to re-run the scan for a different area or facet

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, Tailwind v4, CopilotKit, `@copilotkit/a2ui-renderer` |
| Agent | Python LangGraph (ReAct), FastAPI, `uvicorn` on `:8123` |
| LLM | Gemini 3.5 Flash via `langchain-google-genai` |
| Search | [Linkup SDK](https://docs.linkup.so/) — structured web search for competitor discovery |
| Protocol | [A2UI v0.9](https://a2ui.org/) (declarative UI envelopes), [AG-UI](https://docs.ag-ui.com/) (transport), [A2A](https://a2a-protocol.org/) (multi-agent interop) |

## Run locally

**Prereqs:** Node 20+, pnpm 10+, Python 3.12+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <your-fork-url>
cd A2UIHackathon
pnpm install              # also installs the Python agent via uv sync (postinstall)

cp .env.example .env
# Edit .env — set:
#   GEMINI_API_KEY   → https://aistudio.google.com/apikey (free, no credit card)
#   LINKUP_API_KEY   → https://app.linkup.so (free tier available)

pnpm run doctor           # preflight: Node, pnpm, Python, uv, env vars, ports
pnpm dev                  # boots Next.js (:3000) + FastAPI agent (:8123) concurrently
```

Open `http://localhost:3000`.

### Try it

1. Click **"Run a market scan"** on the landing page → navigates to `/fixed`
2. Type: *"I want to open a Pilates studio in Shoreditch"*
3. The dashboard appears: KPI cards, demand curve, service mix donut, competitor table, scope chips
4. Click a scope chip (e.g. **"Hoxton"**) → dashboard re-renders with data for that area

> **No keys?** Set `OFFLINE=1` in `.env` — the `/fixed` endpoint serves a canned Shoreditch dashboard with no API calls. The catalog gallery at `/catalog` also works without keys.

## Project structure

```
├── src/                        # Next.js frontend
│   ├── app/(pdf)/              # Vantage AI routes (/, /fixed, /dynamic, /catalog)
│   ├── a2ui/                   # A2UI catalog (21 components), theme, surface-bus
│   ├── components/             # React: Brand, SurfaceCanvas, Split, etc.
│   ├── hooks/                  # useTheme, etc.
│   └── lib/                    # Utilities
├── agent/                      # Python LangGraph agents (FastAPI on :8123)
│   ├── src/
│   │   ├── fixed_agent.py      # Market-scan agent (research → dashboard)
│   │   ├── dynamic_agent.py    # Dynamic A2UI Q&A agent
│   │   ├── research_tools.py   # Linkup SDK integration
│   │   ├── catalog.py          # Python mirror of A2UI catalog
│   │   ├── offline_fixed.py    # Offline stub (no Gemini needed)
│   │   └── a2ui/schemas/       # Dashboard JSON layouts
│   └── main.py                 # FastAPI app (/fixed, /dynamic, /legal)
├── a2a/                        # A2A protocol bolt-on (multi-agent interop)
├── other-examples/             # Archived demos (portkit, legal-contract-review)
├── scripts/                    # DX: doctor, smoke, validate-widget, new-widget, etc.
├── fixtures/                   # Test fixtures
├── public/                     # Static assets
├── docker/                     # CI Dockerfiles
├── .github/workflows/          # CI (smoke, frozen-banner, nightly probe)
├── AGENTS.md                   # AI assistant guide (CLAUDE.md, GEMINI.md → symlinks)
├── HACKATHON.md                # Customization recipes (6 seams)
└── FROZEN.md                   # Pinned versions & rationale
```

## Customization seams

Search the repo for `CUSTOMIZATION SEAM`. Full recipes in [HACKATHON.md](HACKATHON.md).

| # | Seam | Files |
|---|------|-------|
| 1 | Re-theme | `src/a2ui/theme.css`, `src/app/(pdf)/pdf-analyst.css`, `src/hooks/use-theme.tsx` |
| 2 | Re-brand | `src/components/pdf-analyst/Brand.tsx` |
| 3 | Swap data source | `agent/src/research_tools.py` (Linkup query), `agent/src/pdf_tools.py` |
| 4 | Add A2UI component | `src/a2ui/catalog/{definitions.ts,renderers.tsx}`, `agent/src/catalog.py` |
| 5 | Swap agent flow | `agent/src/fixed_agent.py`, `agent/src/dynamic_agent.py` |
| 6 | BYO A2A agent | Set `A2A_AGENT_URL`, run `pnpm check-a2a <url>` first |

## Commands

| Command | What it does |
|---------|-------------|
| `pnpm dev` | Boot Next.js + FastAPI agent concurrently |
| `pnpm run doctor` | Preflight env check |
| `pnpm smoke` | Composite gate (validators + pins + offline + canned prompt) |
| `pnpm validate-widget <path>` | Validate widget JSON against A2UI v0.9 |
| `pnpm verify-pins` | Fail if lockfiles drifted from FROZEN.md |
| `pnpm check-a2a <url>` | Validate a partner A2A endpoint |

## Vibe coding

Your AI assistant reads **[AGENTS.md](AGENTS.md)** automatically (cross-tool [agents.md](https://agents.md/) standard). `CLAUDE.md` and `GEMINI.md` are symlinks to the same file.

Also ships:
- **[`.mcp.json`](.mcp.json)** — CopilotKit MCP server for grounded API answers
- **`create-a2ui-widget` skill** at `.claude/skills/`
- **Validators that teach** — `pnpm validate-widget` points at a real JSON template on failure

## Documentation

- **[WELCOME.md](WELCOME.md)** — 200-word orientation
- **[HACKATHON.md](HACKATHON.md)** — build-day playbook with hour-by-hour template
- **[AGENTS.md](AGENTS.md)** — agent guide for AI coding assistants
- **[FROZEN.md](FROZEN.md)** — version-pinning rationale
- **[SUBMITTING.md](SUBMITTING.md)** — submission checklist
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — what we'll merge post-event

## Troubleshooting

- **Chat doesn't respond.** Agent on `:8123` likely failed to start — check terminal for stack trace. Most common: missing `GEMINI_API_KEY`. Run `pnpm run doctor`.
- **Dashboard is empty after submitting.** Check agent logs for Linkup errors — the `LINKUP_API_KEY` may be missing or expired.
- **Windows: missing `CLAUDE.md` / `GEMINI.md`.** Symlinks dropped on checkout. Run `./scripts/sync-memory-files.sh` (Git Bash / WSL) or open `AGENTS.md` directly.
- **`lefthook: Can't find lefthook in PATH`** on commit. Benign — commit still succeeds. Run `pnpm install` once after clone.

## License

MIT. See [LICENSE](LICENSE).

## Attribution

- **A2UI protocol** — [Google](https://github.com/google/A2UI)
- **AG-UI protocol** — [AG-UI Protocol working group](https://github.com/ag-ui-protocol/ag-ui)
- **A2A protocol** — [Linux Foundation + Google](https://github.com/a2aproject/A2A)
- **Linkup** — web search API for AI agents ([linkup.so](https://www.linkup.so/))
- **CopilotKit** — agent-driven UI runtime ([copilotkit.ai](https://copilotkit.ai))
- **Base starter** — [CopilotKit/examples/integrations/langgraph-python](https://github.com/CopilotKit/CopilotKit/tree/main/examples/integrations/langgraph-python)

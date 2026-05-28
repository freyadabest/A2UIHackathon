# `agent/src/` — LangGraph agent source

The Python LangGraph agent that emits A2UI envelopes via CopilotKit. Run
via `pnpm dev:agent` (which delegates to `scripts/run-agent.sh`).

## What lives here

| File | Purpose |
|---|---|
| `a2ui_fixed_schema.py` | **Canonical fixed-schema A2UI example** (`search_flights`). Seam #4 anchor. |
| `a2ui_dynamic_schema.py` | **Canonical dynamic-schema A2UI example** (`generate_a2ui`). Secondary LLM designs the schema. |
| `query.py` | Demo data tool (reads `db.csv`). Seam #3 anchor. |
| `todos.py` | Todo CRUD tools + `AgentState` schema. |
| `db.csv` | Sample dashboards data. |
| `a2ui/schemas/` | JSON schemas loaded by `a2ui_fixed_schema.py`. |
| `widgets/` | (Workstream E) — catalog entries + fixtures per widget. |
| `domains/` | (Workstream E) — domain bundles (data + prompt + widget subset). `DOMAIN=<name>` switches at boot. |

## What you probably want to edit

- **Swap demo data** → `query.py` (Seam #3)
- **Add a new widget** → copy `a2ui_fixed_schema.py:search_flights` (Seam #4)
- **Switch domains** → `agent/src/domains/<name>/` (Seam #5)

## What you probably should NOT edit

- The `ChatOpenAI(...)` call in `../main.py` — FROZEN (see `FROZEN.md`).

See `AGENTS.md` and `HACKATHON.md` for the full customization recipes.

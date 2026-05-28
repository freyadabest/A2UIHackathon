# `agent/` — Python LangGraph agent

The agent process. Boots via `pnpm dev:agent` (which uses `uv` under the
hood and watches for hot reloads).

## Layout

| Path | Purpose |
|---|---|
| `main.py` | Entry point. Wires `ChatOpenAI` (Gemini 2.5 Flash by default) + tools + middleware + system prompt. |
| `src/` | All tool source. See `src/README.md`. |
| `pyproject.toml` | Pinned Python deps (see `../FROZEN.md`). |
| `uv.lock` | Committed lockfile — authoritative for Python deps. |
| `langgraph.json` | LangGraph CLI configuration. |
| `.python-version` | Python toolchain pin. |

## Develop

```bash
# From the repo root
pnpm dev:agent

# Or directly
cd agent
uv run --reload langgraph dev
```

## Customization seams in this directory

- `main.py` system prompt — first line of "make it about my domain"
- `main.py` `tools=[...]` — register new widget tools here
- `src/query.py` — Seam #3 (swap demo data)
- `src/a2ui_fixed_schema.py` — Seam #4 (add a widget)

## What you probably should NOT touch

- The `ChatOpenAI(...)` block in `main.py` — the model ID and base URL
  are FROZEN. See `../FROZEN.md` § LLM provider and the inline anchor
  comment for the full story (including why NOT Gemini 3.5 Flash).
- `pyproject.toml` versions — pinned. Pre-commit hook will reject drift.

See `../AGENTS.md` and `../HACKATHON.md` for recipes.

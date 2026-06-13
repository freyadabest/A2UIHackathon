# `src/app/` — Next.js 16 App Router

This is the web app. Next.js 16 + React 19 + Tailwind 4. The default demo is
**pdf-analyst** (chat-with-your-PDF → agent-built A2UI surfaces).

## What lives here

| File / dir | Purpose |
|---|---|
| `layout.tsx` | Root layout. `<html>` + `<ThemeProvider>` only — the CopilotKit provider mounts per route group. |
| `(pdf)/` | The pdf-analyst route group: `/` (landing), `/fixed` (dashboard), `/dynamic` (Q&A surfaces), `/catalog` (component gallery). Its `layout.tsx` mounts the CopilotKit provider + the A2UI catalog. |
| `(legal)/` | The legal-contract-review example's route group (UI currently a WIP stub; the `/legal` agent endpoint works). |
| `other-examples/` | Gallery page that enumerates `other-examples/*/EXAMPLE.json` manifests. |
| `globals.css` | Host `:root` tokens + Tailwind 4 directives + pinned-CopilotKit CSS workarounds (see the labelled block at the end). |
| `(pdf)/pdf-analyst.css` | Shell brand tokens, scoped to `.pdf-analyst-root` (Seam #1). |
| `api/copilotkit-pdf/` | The pdf-analyst runtime route → FastAPI agents on `:8123` (`/fixed`, `/dynamic`). |
| `api/copilotkit/` | The host (v1) runtime route — serves the legal example and carries the A2A bolt-on (Seam #6). |

The A2UI catalog itself (definitions + renderers) lives at `src/a2ui/`.

## What you probably want to edit

- **A2UI surface theme** → `src/a2ui/theme.css` (Seam #1)
- **Shell brand tokens** → `(pdf)/pdf-analyst.css` (Seam #1)
- **Header / branding / hero copy** → `src/components/pdf-analyst/Brand.tsx` (Seam #2)
- **Add a catalog component** → `src/a2ui/catalog/{definitions.ts,renderers.tsx}` + `agent/src/catalog.py` (Seam #4)

## What you probably should NOT edit

- The `<CopilotKit>` provider config in `(pdf)/layout.tsx` — versions are
  pinned for a reason (see `FROZEN.md`).
- `api/copilotkit-pdf/route.ts`'s `injectA2UITool: false` — the dynamic
  agent's `generate_a2ui` Python tool depends on it (the docstring in
  `agent/src/dynamic_agent.py` explains the orphan-`function_call` trap).
- The legacy PortKit-era components (`BrandFrame.tsx`, `example-layout/`,
  `ModeToggle.tsx`, …) — they're not mounted by the pdf-analyst routes.

See `AGENTS.md` and `HACKATHON.md` for the full customization recipes.

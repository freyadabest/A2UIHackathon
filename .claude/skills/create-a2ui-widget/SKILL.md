---
name: create-a2ui-widget
description: Adds a new A2UI component to the CopilotKit A2UI hackathon starter's shared catalog, end-to-end. Coordinates the 3-surface component dance (TypeScript definition + Zod prop schema, React renderer, agent prompt mirror) so components actually render instead of ending up half-finished. Use when the hacker says "add a widget", "add a component", "scaffold a card", "build me a [domain] visual", "build me a metrics card", "add an A2UI widget", "make a new component", or asks for a new generative-UI surface in this repo. Anchors against the live catalog at `src/a2ui/catalog/definitions.ts`. Enforces the AGENTS.md hard rules — never bump @copilotkit/* versions, always run `pnpm validate-widget` after editing widget JSON, always run `pnpm smoke` before declaring done. Don't use for re-theming (Seam #1 — edit `src/a2ui/theme.css` + `src/app/(pdf)/pdf-analyst.css`), swapping demo data (Seam #3 — edit `agent/src/pdf_tools.py`), swapping the agent flow (Seam #5 — edit `agent/src/fixed_agent.py` / `agent/src/dynamic_agent.py`), or wiring an A2A partner agent (Seam #6 — `pnpm check-a2a <url>`).
version: 2.0.0
---

# Create A2UI Component

## When To Use

Trigger this skill whenever the hacker wants to add a new A2UI component — a
new declarative UI primitive the agent can render. Trigger phrases include:

- "add a widget" / "add a component"
- "scaffold a card"
- "build me a [domain] visual" (e.g. "build me a portfolio card", "build me a recipe card")
- "build me a metrics card"
- "add an A2UI widget"
- "make a new A2UI component"
- "I want a widget that shows [X]"

Do NOT trigger this skill for:

- Re-theming colors / fonts — Seam #1: edit `src/a2ui/theme.css` (A2UI
  surface tokens) + `src/app/(pdf)/pdf-analyst.css` (shell brand tokens).
- Re-branding the shell — Seam #2: edit `src/components/pdf-analyst/Brand.tsx`.
- Swapping demo data — Seam #3: the uploaded PDF is the data; tune
  `agent/src/pdf_tools.py`.
- Swapping the agent flow — Seam #5: edit `agent/src/fixed_agent.py` /
  `agent/src/dynamic_agent.py`.
- Wiring an external A2A agent — Seam #6: run `pnpm check-a2a <url>` then set
  `A2A_AGENT_URL`.

## The catalog model (read this before editing)

The pdf-analyst catalog is **one shared design system**: 21 platform-agnostic
component definitions paired with React renderers, defined entirely in
TypeScript. Both agents (`/fixed` and `/dynamic`) compose surfaces from the
same catalog, so adding a component makes it available everywhere. There is
**no per-widget JSON + fixture + Python tool** in this flow — that older
"5-surface widget dance" belongs to the archived PortKit demo under
`other-examples/portkit/` and must not be followed here. There is no
`agent/src/widgets/`, no `agent/src/tools/`, no `agent/src/domains/`, and no
`EnvelopeInspector` in the live repo.

## The 3-Surface Component Dance

The #1 reason components ship half-finished is that hackers (and their AI
assistants) touch one or two of the three surfaces and call it done. A
component needs ALL THREE. Skip one and either nothing renders or the agent
never emits it.

1. **Definition** — `src/a2ui/catalog/definitions.ts`. Add an entry to the
   `definitions` object: a one-line `description` plus a Zod `props` schema.
2. **Renderer** — `src/a2ui/catalog/renderers.tsx`. Add the matching React
   component to the `renderers` map.
3. **Prompt mirror** — `agent/src/catalog.py`. Add a one-line summary of the
   component to `CATALOG_PROMPT` so the agent knows it exists and what props
   it accepts.

## Hard Rules (from AGENTS.md — do not violate)

- **Never run `pnpm install` for a new `@copilotkit/*` version.** Versions
  are pinned in `FROZEN.md`. The pre-commit hook will reject any drift.
- **Always run `pnpm validate-widget <path>`** after editing any widget/schema
  JSON (e.g. `agent/src/a2ui/schemas/dashboard.json`).
- **Always run `pnpm smoke`** before declaring the work done.
- **Don't write a new React renderer system for A2UI primitives.** Renderers
  go in the catalog's `renderers.tsx` map; `@copilotkit/a2ui-renderer` owns
  the rendering pipeline.
- **Don't reintroduce an envelope-inspector rail.** The A2UI output is
  surfaced by the in-canvas `SurfaceCanvas` + the chat `MirrorRenderer` pill.

## Procedure

### Step 1 — Read the canonical examples

Pick a `PascalCase` name (e.g. `Timeline`, `RecipeCard`, `MetricGrid`).

Read these two files end-to-end before writing anything:

- `src/a2ui/catalog/definitions.ts` — the 21 shipped definitions. Note the
  helpers at the top: `childRef` / `childrenRef` (component-ID references)
  and `stringOrPath` (props that may be a literal or a `{path}` data
  binding). Note `CATALOG_ID` — do not change it.
- `src/a2ui/catalog/renderers.tsx` — the matching React renderers. The
  binder hands renderers **resolved** props (literals, not `{path}` objects).

For a chart-shaped component, copy the shape of `BarChart`; for a
content-shaped one, copy `Callout` or `StatCard`.

### Step 2 — Add the definition

In `src/a2ui/catalog/definitions.ts`, add to the `definitions` object:

```ts
Timeline: {
  description:
    "Vertical list of dated events. Use for chronologies, changelogs, milestones.",
  props: z.object({
    events: z.union([
      z.array(z.object({ date: z.string(), label: z.string() })),
      z.object({ path: z.string() }),
    ]),
    title: stringOrPath.optional(),
  }),
},
```

Match the Zod version the repo already uses (`import { z } from "zod"` at the
top of the file) — do not add a new zod dependency. Mismatched Zod majors make
the binder silently treat every prop as static.

### Step 3 — Add the renderer

In `src/a2ui/catalog/renderers.tsx`, add the matching entry to the
`renderers` map. Style it with the A2UI surface tokens from
`src/a2ui/theme.css` (`--card`, `--border`, `--muted-foreground`, `--accent`,
`--radius`) so it inherits any re-theme automatically. Use `recharts` for
charts (already a dependency) — copy an existing chart renderer's shape.

### Step 4 — Mirror it in the agent prompt

In `agent/src/catalog.py`, add one line to `CATALOG_PROMPT` under the right
section heading, matching the existing format:

```
- **Timeline** { events: [{date,label}] | {path}, title?: string|{path} }
    Vertical list of dated events. Use for chronologies and milestones.
```

If you skip this, the component renders fine in `/catalog` but the agent
never emits it — the prompt is the only way the LLM knows it exists.

### Step 5 — (Optional) Use it in the fixed dashboard

If the fixed `/fixed` dashboard should include the new component, add it to
the hand-authored layout at `agent/src/a2ui/schemas/dashboard.json` and
extend `render_dashboard`'s typed inputs in `agent/src/fixed_agent.py` if it
needs new data. Then:

```bash
pnpm validate-widget agent/src/a2ui/schemas/dashboard.json
```

The `/dynamic` agent needs no extra wiring — it composes from the prompt
mirror automatically.

### Step 6 — Verify

```bash
pnpm typecheck          # the Zod schema + renderer compile
pnpm validate-widget agent/src/a2ui/schemas/dashboard.json   # if you touched it
pnpm test:widgets
pnpm smoke              # the load-bearing final gate
```

Then run the live check: `pnpm dev`, open `/dynamic`, and ask a question
that should trigger the component (e.g. "show the milestones as a timeline").
Confirm the canvas paints it and the `MirrorRenderer` pill echoes the surface.

## Scaffolding helper

`pnpm new-widget <name>` seeds a catalog schema + fixture JSON pair under
`agent/src/a2ui/schemas/` and prints these same next steps. It's optional —
the JSON files matter only if you want the component exercised by
`pnpm test:widgets` / a fixed layout; the TypeScript catalog is the source
of truth.

## Common Failure Modes (audit before declaring done)

- **Added the definition but not the prompt mirror.** The agent never emits
  the component. Most common failure in this layout.
- **Added the definition but no renderer (or vice versa).** The surface
  arrives but that node renders nothing. Definition and renderer keys must
  match exactly (case-sensitive).
- **Invented a new `CATALOG_ID`.** `createSurface` resolves renderers by
  catalog ID; `src/a2ui/catalog/definitions.ts` and `agent/src/catalog.py`
  must keep the identical ID.
- **Used `{path}` bindings on props whose schema doesn't accept them.** Wrap
  the prop type with the `stringOrPath`-style union if it should be bindable.
- **Data keys don't match the `path` references.** If the component binds
  `{ "path": "/items" }`, the agent must put `items` at the data-model root
  via `updateDataModel`.
- **Followed the archived PortKit flow** (`agent/src/widgets/*.json` +
  `agent/src/tools/*.py` + `domains/default/tools.py`). Those paths don't
  exist in the live repo — if you find yourself creating them, stop and
  re-read "The catalog model" above.
- **Bumped a `@copilotkit/*` version.** The pre-commit hook rejects the
  commit. Revert `package.json` and `pnpm-lock.yaml`.
- **Skipped `pnpm smoke`.** Smoke is the canonical "is this done?" signal.

## Quick Checklist (paste into the chat as a TODO before starting)

- [ ] Step 1: read `src/a2ui/catalog/definitions.ts` + `renderers.tsx`
- [ ] Step 2: add the definition (description + Zod props)
- [ ] Step 3: add the React renderer (A2UI surface tokens, recharts if a chart)
- [ ] Step 4: mirror a one-line summary in `agent/src/catalog.py` `CATALOG_PROMPT`
- [ ] Step 5 (optional): wire into `agent/src/a2ui/schemas/dashboard.json` + `fixed_agent.py`
- [ ] Step 6: `pnpm typecheck`, `pnpm validate-widget` (for JSON), `pnpm test:widgets`, `pnpm smoke` — all green

## Canonical References

- Live catalog definitions: `src/a2ui/catalog/definitions.ts`
- Live catalog renderers: `src/a2ui/catalog/renderers.tsx`
- Agent prompt mirror: `agent/src/catalog.py` (`CATALOG_ID` + `CATALOG_PROMPT`)
- Fixed dashboard layout: `agent/src/a2ui/schemas/dashboard.json` (+ `agent/src/fixed_agent.py`)
- Dynamic-schema flow: `agent/src/dynamic_agent.py` (`generate_a2ui`)
- Hard rules and seam map: `AGENTS.md` (also `CLAUDE.md` / `GEMINI.md`)
- Recipe: `HACKATHON.md` §4
- Pinned versions: `FROZEN.md`
- A2UI v0.9 spec: https://a2ui.org/specification/v0.9-a2ui/
- A2UI Composer: https://a2ui-composer.ag-ui.com/
- Archived PortKit widget flow (do NOT follow at root): `other-examples/portkit/`

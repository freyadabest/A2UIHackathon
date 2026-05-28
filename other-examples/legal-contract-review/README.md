# Contract Review Copilot

> **Heads up — read this first.**
>
> Most widget work belongs in the `create-a2ui-widget` skill (single catalog, pure-data widgets). This example deliberately goes one layer deeper — it demonstrates the *custom catalog registration* step that the skill marks "out of scope here." If you want to add a widget to the dashboard, use the skill. If you want a new visual identity (paper, terminal, kiosk) with net-new component primitives, this is the pattern.

A paper-styled contract reviewer where an AI agent flags risky clauses, drops margin notes, and proposes redlines. Built as a sub-repo under `/other-examples/` to demonstrate registering a *second* A2UI catalog (`copilotkit://legal-paper-catalog`) alongside the main dashboard catalog.

See the [parent plan §0.5](https://www.notion.so/36e3aa38185281e49674f95ea7039b90) for why this example exists separately from the `create-a2ui-widget` skill.

---

## Setup

Open [`/other-examples/legal-contract-review`](http://localhost:3000/other-examples/legal-contract-review) in the browser once the starter is running.

Requires `GEMINI_API_KEY` in your `.env` (same one the dashboard demo uses).

If the starter isn't running yet, follow the root `README.md` first — this example shares the parent's `pnpm dev` entry point, agent runtime, and CopilotKit route.

---

## What you'll see

- A paper-styled document (warm off-white, serif body, reading column)
- An agent that reviews the contract clause-by-clause
- Risk badges + right-margin notes for flagged clauses
- Inline redlines with accept/reject actions
- A top-line verdict summary

Sample documents live under `agent/data/` (NDA + SaaS agreement).

---

## Fork notes — what's actually portable

This folder is a **content unit**, not a build-system unit. The sub-repo layout under `/other-examples/<name>/` is a folder-structure convention so hackers know where to find each piece — but copy-pasting it into a fresh repo also requires surgery on the host.

Per [plan §3.1 honesty callout](https://www.notion.so/36e3aa38185281e49674f95ea7039b90), if you fork this folder into a new repo you also need:

1. The parent's exact `@copilotkit/*` pins (`package.json`)
2. A working `src/app/api/copilotkit/[[...slug]]/route.ts` shell
3. The route-group `layout.tsx` that mounts `<CopilotKit>`
4. Tailwind 4 + `globals.css` + `ThemeProvider`
5. A `langgraph.json` entry referencing the agent dir
6. Pinned Python deps from `agent/pyproject.toml`

Portable inside this starter; portable across repos with documented surgery.

**Also:** if you don't actually need a second catalog (you just want new widgets), the `create-a2ui-widget` skill is a much shorter path. Re-read the callout at the top of this README.

---

## Disclaimer

**Demo only — not legal advice.** Fictional parties, fictional contracts, fictional flagged clauses. Do not use the output of this example to evaluate a real agreement.

## A note on dark mode

This example uses a fixed light theme for the document surface; the rest of the app honors your dark-mode preference. The warm off-white paper is load-bearing for the "printed contract" affordance, so the paper catalog scopes `color-scheme: light` under `[data-catalog-style="legal-paper"]` (see `catalog/theme.css`). Toggle the global theme freely — only the paper surface stays light.

---

## Layout

```
legal-contract-review/
├── README.md         (you are here)
├── FRICTION.md       (dogfooding log — every workaround / surprise / gap)
├── EXAMPLE.json      (manifest read by the example gallery)
├── catalog/          (Zod schemas + React renderers for the Paper catalog)
├── agent/            (LangGraph Python package — graph, tools, sample data)
└── schemas/          (component-tree adjacency lists + test fixtures)
```

See plan §3 for the full layout convention. The Next.js route lives at `src/app/(legal)/legal-contract-review/page.tsx` as a thin shim that imports from this folder — Next App Router requires routes under `src/app/`, so the *content* lives here and the *mount point* lives there.

---

## Build engineer retro

_Honest version. Read [FRICTION.md](./FRICTION.md) for the full log._

Building this through the documented hackathon paths only — `pnpm new-widget`, the `create-a2ui-widget` skill, `AGENTS.md`, in-tree READMEs — surfaced more rough edges than the dashboard demo does. Three rows became filed P0 issues on day one: `pnpm validate-widget` rejected the shipped `flight_card.json` ([#2](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/2)), `pnpm test:widgets` came up red against the shipped fixtures ([#3](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/3)), and the plan's langgraph multi-graph fix was incomplete under the path-based loader, requiring sys.path injection with absolute imports ([#4](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/4)). Every single blitz agent — seven for seven — hit `lefthook: Can't find lefthook in PATH` on commits from worktrees ([#5](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/5)).

What I'd want you to know: there's no `pnpm new-example` generator yet (FRICTION P2), `tsc` and `dev:ui` don't work cleanly from worktrees (FRICTION P2), and three incompatible "fixture" shapes coexist in the starter (FRICTION P1) — the validator's `{components, data}` shape is the authoritative one when in doubt. The heavy catalog slot (973 LOC, four files) hit context exhaustion mid-flight and needed a finalize subagent (FRICTION P1) — decompose multi-file builds and write the cheapest aggregator first. The validator's "canonical example" error message points at a Python file instead of a JSON template (FRICTION P1) — open the schema JSON, not the `.py`. Build straight ahead, log the friction, file the issues; that *is* the contribution.

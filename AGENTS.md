# CopilotKit A2UI Hackathon Starter — Agent Guide

You are working in a hackathon starter for the **Generative UI Hackathon**
(London slot, Google CSG venue, May 2026). The hacker wants to customize this
app to demo their own domain inside the build window of a 5-hour hackathon.
Speed and clarity beat completeness. Pattern-match aggressively — copy the
canonical examples named in this guide rather than inventing new ones.

## What this repo is

A Next.js + LangGraph + CopilotKit + A2UI v0.9 starter that demonstrates
**agent-driven generative UI**. Three subsystems:

- `src/app/` — Next.js 16 + React 19 + Tailwind 4 web app
- `agent/` — Python LangGraph agent emitting A2UI envelopes via CopilotKit
- `a2a/` — Optional A2A bolt-on for Track 1 multi-agent interop (dormant
  until `A2A_AGENT_URL` is set)

The agent emits A2UI v0.9 declarative UI envelopes (`createSurface`,
`updateComponents`, `updateDataModel`). The renderer turns them into React.
Read `HACKATHON.md` for the customization recipes.

## Hard rules

1. **Versions are pinned.** Do NOT bump `@copilotkit/*`, `langchain*`, or
   `langgraph*` versions without explicit instruction. See `FROZEN.md`. The
   pre-commit hook will reject `@copilotkit/*` drift.
2. **Always run `pnpm validate-widget <path>`** after editing any widget JSON.
3. **Always run `pnpm smoke`** before declaring work done. `smoke` is a
   composite gate: validators + pin check + offline path + canned prompt.
4. **Default LLM is Gemini 2.5 Flash via OpenAI compat.** Do not change
   `base_url` or `model` in `agent/main.py` unless told. Gemini 3.x is a
   known trap (thought-signature requirement that `langchain-openai` does not
   yet implement). See `FROZEN.md` § LLM provider.
5. **Don't edit `src/components/EnvelopeInspector.tsx`** unless asked. It is
   the hackathon's "show the wire" affordance — surfaces must stay visible.
6. **Don't write new React renderers for A2UI primitives.** Use the catalog
   + theme system. The renderer is provided by `@copilotkit/a2ui-renderer`.

## Customization seams

These are the six grep-anchored seams a hacker (or you) edit to make this
starter their own. Search for `CUSTOMIZATION SEAM` to find each one in code.

1. **Re-theme** → `src/lib/a2ui-theme.css` (CSS variables) + `src/hooks/use-theme.tsx`
2. **Re-brand the shell** → `src/components/BrandFrame.tsx` (header, logo, palette accents)
3. **Swap demo data** → `agent/src/query.py` (or `agent/src/domains/<active>/data/`)
4. **Add an A2UI widget (fixed schema)** → copy
   `agent/src/a2ui_fixed_schema.py:search_flights`, declare in
   `src/app/api/copilotkit/route.ts` schema array, register in `agent/main.py`
5. **Switch domain** → set `DOMAIN=<name>` in `.env`; canonical stub at
   `agent/src/domains/shopping`
6. **BYO A2A agent** → set `A2A_AGENT_URL`; run `pnpm check-a2a <url>` first.
   Wired in `src/app/api/copilotkit/route.ts`.

`HACKATHON.md` has the full step-by-step recipe for each seam.

## Canonical examples

When the hacker asks for a new something, grep-find and copy the canonical:

- **Fixed-schema A2UI widget:** `agent/src/a2ui_fixed_schema.py:search_flights`
  (returns `a2ui.render(operations=[...])` with `create_surface` →
  `update_components` → `update_data_model`)
- **Dynamic-schema A2UI:** `agent/src/a2ui_dynamic_schema.py:generate_a2ui`
  (secondary LLM produces the component tree on demand)
- **A2UI envelope (raw JSON):** `agent/src/widgets/*.fixture.json`
- **Brand shell:** `src/components/BrandFrame.tsx`
- **Theme tokens:** `src/lib/a2ui-theme.css`

## Commands

| Command | What it does |
|---|---|
| `pnpm doctor` | Preflight env check (Node, pnpm, Python, uv, env vars, ports) |
| `pnpm dev` | Boot Next.js + Python agent concurrently |
| `pnpm smoke` | Composite gate (validators + pins + offline + canned prompt) |
| `pnpm validate-widget <path>` | Validate a widget JSON against A2UI v0.9 |
| `pnpm check-a2a <url>` | Validate a partner A2A endpoint |
| `pnpm explain <topic>` | Print the right HACKATHON.md section (`themes`, `widgets`, `a2a`, `data`, `branding`, `domain`) |
| `pnpm new-widget <name>` | Scaffold from `search_flights` template |
| `pnpm theme:reset` | Revert theme to defaults |
| `pnpm verify-pins` | Fail if lockfiles drifted from `FROZEN.md` |

## Slash command vocabulary (for AI assistants)

When the hacker says:

- **"add a widget"** → follow `HACKATHON.md` §4 (prefer fixed-schema for
  demo predictability). Copy `search_flights`. Run the **5-surface dance**:
  catalog entry + fixture + Python tool + TS schema declaration + prompt
  hint. Run `pnpm validate-widget` then `pnpm smoke` before declaring done.
- **"theme it for X"** → only edit `src/lib/a2ui-theme.css` and
  `src/hooks/use-theme.tsx`. Don't restructure components. Don't bump deps.
- **"re-brand it"** → edit `src/components/BrandFrame.tsx`. Don't touch the
  envelope inspector or chat affordances.
- **"make it about Y"** (e.g. shopping, healthcare) → swap demo data in
  `agent/src/query.py` and the system prompt in `agent/main.py`. Don't
  restructure. Reference `agent/src/domains/shopping/` as the pattern.
- **"connect to another agent"** → run `pnpm check-a2a <url>` first; only
  then set `A2A_AGENT_URL` in `.env`. See HACKATHON.md §6.

## Anti-patterns (don't do this)

- Don't run `pnpm install` against a new `@copilotkit/*` version.
- Don't add new top-level dependencies without checking if base already has
  an equivalent (e.g. don't pull in `framer-motion` if the existing
  CSS-transition path suffices).
- Don't replace the envelope inspector with a toggle. It must stay visible.
- Don't hand-roll React renderers for A2UI primitives. Use the catalog +
  theme system. (`@copilotkit/a2ui-renderer` owns rendering.)
- Don't change `agent/main.py`'s `ChatOpenAI(...)` model call. The provider,
  base URL, and model ID are FROZEN — see `FROZEN.md`.
- Don't fabricate seams. If `CUSTOMIZATION SEAM` doesn't grep, the hacker is
  asking you to invent one. Push back and ask which existing seam fits.

## Claude Code users

The "slash command vocabulary" above lists recipes, not real CLI commands.
Follow them when the hacker types them in chat. Skills live at:
`.claude/skills/create-a2ui-widget/SKILL.md` (when Workstream F lands).

Useful grep starting points:
- `grep -r "CUSTOMIZATION SEAM" .` — find all seams in two seconds
- `grep -r "Pattern to copy" .` — find canonical examples
- `agent/src/a2ui_fixed_schema.py` — read this top-to-bottom before adding a widget

## Gemini CLI users

`.gemini/settings.json` (added in Workstream F) sets trust roots and adds
`AGENTS.md` to the context filename list. The starter is fully trusted.

Useful one-liners:
- `gemini -p "explain seam #4 from HACKATHON.md"` — see the recipe
- `gemini -p "add a recipe-card widget patterned after search_flights"`

## Cursor / Windsurf / Codex users

`AGENTS.md` (this file) is the cross-tool standard ([agents.md](https://agents.md/),
Linux Foundation) read natively by Cursor, Windsurf, Codex CLI, Kilo Code,
Aider, and Sourcegraph Cody. No extra config needed.

`.vscode/settings.json` + `.vscode/extensions.json` (added in Workstream F)
enable the CopilotKit A2UI catalog preview extension and recommend it on
first open.

## When in doubt

1. `grep -r "CUSTOMIZATION SEAM" .` — find the seam.
2. Read the canonical example named in the anchor comment.
3. Copy its shape. Swap content. Run `pnpm validate-widget` then `pnpm smoke`.
4. If the hacker is asking for something that doesn't have a seam, push back
   before inventing new architecture. The build window is 5 hours.

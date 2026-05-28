# Friction Log — Legal Contract Review

Built as a dogfooding exercise per [plan §0.6](https://www.notion.so/36e3aa38185281e49674f95ea7039b90). Every row converts to a GitHub issue with the `dogfood-friction` label (see plan §0.7 for the label taxonomy + triage cadence).

The engineer building this example is a **proxy hackathon attendee**: documented paths only (`pnpm new-widget`, `create-a2ui-widget` skill, `AGENTS.md`, in-tree READMEs, validators), AI coding assistant for the typing, no insider help from starter authors. If a documented path doesn't unblock you, that *is* the issue — log it here.

End of each build day (17:00): convert every row in **Open** to a GitHub issue via the `to-issues` skill, then move it to **Converted to issues**.

---

## Row template

Each row uses the §0.7 template:

```markdown
## [P0/P1/P2] One-line title
- **Encountered while:** [step from create-a2ui-widget skill / this plan / AGENTS.md section]
- **What I tried:** [the documented path]
- **What happened:** [error / confusion / missing piece — paste actual error if any]
- **What I wanted:** [the right outcome]
- **Suggested fix:** [if obvious; else "needs design"]
- **Who hits this:** [hackathon attendee profile — Claude Code / Gemini CLI / Cursor / human-only / new-to-LangGraph / etc.]
- **Filed as:** [#NNN]
```

Severities (from §0.7):

- **P0 / `severity:P0-blocker`** — hacker cannot proceed via documented path
- **P1 / `severity:P1-pain`** — works but with significant unintended difficulty
- **P2 / `severity:P2-polish`** — minor wording, error-message clarity, doc gaps

---

## Open

### Pending issue filing (P2 / P3 — to be batch-filed in next triage pass)

## [P2] PLAN.md in-tree doesn't have §0.7 (friction protocol) — only Notion has it
- **Encountered while:** B1 reading the spec's reference to §0.7
- **What I tried:** `grep -n -i "friction\|0\.7" PLAN.md`
- **What happened:** Zero matches for "friction" or "0.7" — only the Notion URL in the orchestrator prompt has the §0.7 content
- **What I wanted:** PLAN.md in-tree should mirror §0.7 or have a clear pointer ("§0.7 lives in Notion until v4 lands")
- **Suggested fix:** Mirror §0.7 into PLAN.md, or add a `## §0.7 (Notion canonical)` stub with the URL
- **Who hits this:** claude-code, gemini-cli, cursor — any AI agent without web access to the Notion link

## [P2] No template file or generator for sub-repo layout
- **Encountered while:** B2 scaffolding `other-examples/legal-contract-review/` from scratch (plan §3)
- **What I tried:** Looked for an existing template under `other-examples/`, looked for `pnpm new-example` script, grepped AGENTS.md / HACKATHON.md / README.md for `other-examples` mentions
- **What happened:** Nothing existed. Had to hand-author every file from the plan's prose layout (§3) plus the §3.2 schema dump
- **What I wanted:** A `pnpm new-example <name>` generator, or at minimum an AGENTS.md / HACKATHON.md section saying "Sub-repo examples live under `other-examples/<id>/`; see `other-examples/README.md` for the layout"
- **Suggested fix:** Ship the `pnpm new-widget --example` generator referenced in plan §10 Open question #1 before Jun 13
- **Who hits this:** Every hackathon attendee trying to add a second example

## [P2] tsc not available from worktree path
- **Encountered while:** B3 verifying typecheck after route-group restructure
- **What I tried:** `pnpm exec tsc --noEmit` from the worktree
- **What happened:** `Command "tsc" not found` because the worktree has no `node_modules` (only the main repo does)
- **What I wanted:** Either `pnpm typecheck` wired as a real `package.json` script that works from a worktree, or `node_modules` symlinked into worktrees, or documentation on how to typecheck from a worktree
- **Suggested fix:** Add `"typecheck": "tsc --noEmit"` to `package.json` scripts and ensure it works from a worktree
- **Who hits this:** All AI assistants using worktree-based workflows (Claude Code blitz, Cursor isolated branches, etc.)

## [P2] `pnpm dev:ui` cannot smoke-test changes in a worktree
- **Encountered while:** B3 trying AC5 "5s dev:ui verify build compiles"
- **What I tried:** `pnpm dev:ui` from the worktree
- **What happened:** The dev server is rooted in the main repo, not the worktree — worktree changes are invisible to it
- **What I wanted:** A way to spin up a worktree-scoped dev server, or documentation that the only worktree-safe smoke is typecheck
- **Suggested fix:** Document this limitation in AGENTS.md; consider per-worktree dev port allocation
- **Who hits this:** Claude Code blitz agents (this case); anyone doing parallel worktree development

## [P2] No documented convention for the widget-mirror-vs-canonical-location question
- **Encountered while:** B6 deciding whether to symlink or duplicate the schema between `other-examples/.../schemas/` and `agent/src/widgets/legal/`
- **What I tried:** Looked at `agent/src/widgets/README.md` and the plan; neither addressed sub-repo example mirroring
- **What happened:** Had to make the call (chose duplication for cross-platform safety)
- **What I wanted:** A one-line policy in `agent/src/widgets/README.md` for the example-mirror case
- **Suggested fix:** Document: "Sub-repo examples may duplicate their widget JSONs here for `pnpm validate-widget` / `pnpm test:widgets` discovery. Keep duplicate copies byte-identical at commit time."
- **Who hits this:** Anyone adding a sub-repo example with custom widgets

## [P2] node_modules not pre-installed in fresh worktree
- **Encountered while:** B6's first `pnpm validate-widget` invocation
- **What I tried:** `pnpm validate-widget ...`
- **What happened:** `sh: tsx: command not found`. Required `pnpm install --frozen-lockfile` (12s) before scripts would run
- **What I wanted:** Worktrees inheriting node_modules from the parent, or a documented setup step for fresh worktrees
- **Suggested fix:** Add `pnpm install` to the blitz worktree setup steps, OR symlink `node_modules/` into worktrees, OR document this in the worktree skill
- **Who hits this:** Any blitz agent that runs scripts in a fresh worktree

## [P2] langgraph 0.7.101 dockerfile mis-routes second dependency's graph path
- **Encountered while:** B5 testing `langgraph build` / docker output
- **What I tried:** Default `langgraph dockerfile` after adding second dep to `dependencies` array
- **What happened:** Second dep's graph path is mis-rewritten in the generated `LANGSERVE_GRAPHS` env var — points to `/deps/agent/graph.py` but the file is copied to `/deps/agent_1/graph.py`
- **What I wanted:** Either langgraph CLI fixes the multi-dep dockerfile output, or this starter ships a custom Dockerfile that handles it
- **Suggested fix:** Custom Dockerfile in the example, OR upstream a CLI fix
- **Who hits this:** Anyone deploying multi-graph langgraph to Docker (not affecting hackathon dev flow, but blocks production deploy demos)

## [P3] AC1 grep ambiguity — `grep 'CopilotKit'` matches brand text vs provider
- **Encountered while:** B3 confirming AC1 ("CopilotKit out of root layout")
- **What I tried:** `grep -l 'CopilotKit' src/app/layout.tsx`
- **What happened:** Still matched `<title>CopilotKit</title>` (page brand text, preserved intentionally). Stricter `grep -E '<CopilotKit|@copilotkit/react-core'` returned nothing as intended
- **Suggested fix:** Tighten future AC patterns to specifically match the import/provider use, not the literal string
- **Who hits this:** AI assistants following strict ACs verbatim

## [P3] Worktree-aware env loading for langgraph
- **Encountered while:** B5 running `langgraph dev` from worktree's `agent/`
- **What happened:** Couldn't find `worktree-root/.env` (only main-checkout `.env` exists). Required manual `export GEMINI_API_KEY=...`. Pre-existing condition — sample_agent has the same issue from a worktree
- **Suggested fix:** Document this limitation; `pnpm dev` from main is unaffected
- **Who hits this:** Anyone running langgraph from a worktree without copying `.env`

## [P3] setuptools auto-discovery package name collision
- **Encountered while:** B5 setting up `pyproject.toml` in `other-examples/.../agent/`
- **What happened:** setuptools auto-discovery picks `agent` as the package name (same as project-root `agent/`). Would collide if both installed in same env
- **Workaround:** sys.path injection sidesteps it in practice
- **Suggested fix:** Rename inner package dir to avoid collision, or explicit `packages = ["legal_review_agent"]` in pyproject

---

## Converted to issues

### [P0] pnpm validate-widget rejects shipped flight_card.json (wrapper shape mismatch)
- **Filed as:** [#2](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/2)
- **Discovered by:** B6 (Wave 1 blitz, 2026-05-28)

### [P0] pnpm test:widgets red day-one — shipped fixture shapes don't match validator
- **Filed as:** [#3](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/3)
- **Discovered by:** B6 (Wave 1 blitz, 2026-05-28)

### [P0] Plan §6.1 langgraph multi-graph fix is incomplete — relative imports break under path-based loader
- **Filed as:** [#4](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/4)
- **Discovered by:** B5 (Wave 1 blitz, 2026-05-28)
- **Workaround applied:** sys.path injection in `other-examples/legal-contract-review/agent/graph.py` with absolute imports

### [P1] lefthook 'Can't find lefthook in PATH' on every commit from a worktree (cross-cutting)
- **Filed as:** [#5](https://github.com/jerelvelarde/london-a2ui-a2a-starter/issues/5)
- **Discovered by:** B1, B2, B3, B4, B4-finalize, B5, B6 — 5/5 commit operations. Escalated from P2 → P1 due to universal hit rate.

### To be filed in next triage pass (P1)

## [P1] Three incompatible "fixture" shapes coexist in the starter
- **Encountered while:** B6 trying to author `contract_review.fixture.json` that satisfies `pnpm validate-widget`
- **What happened:** The prompt skeleton (`{name, surfaceId, catalogId, data}`) disagrees with the validator (`{surfaceId, catalogId, components, data}`) AND with the shipped fixture files (`{name, surfaceId, envelopes: [...]}`). A hacker hits a coin-flip on which one they pick up.
- **Suggested fix:** Pick one. The validator's `{components + data}` shape is the cheapest to settle on because the validator is the authority.
- **Who hits this:** Every hackathon attendee authoring a widget fixture.

## [P1] validate-widget error messages point at .py file instead of canonical JSON
- **Encountered while:** B6 reading validate-widget's "Canonical example:" hint
- **What happened:** validate-widget points at `agent/src/a2ui_fixed_schema.py:search_flights` as the canonical, but the actual nearest-shape JSON example for the bare-array schema is `agent/src/a2ui/schemas/flight_schema.json`. A hacker reading the error opens the Python file and finds a Python function, not a JSON template to mirror.
- **Suggested fix:** Point the canonical reference at the JSON file, not the Python tool, OR ship the JSON path-anchor inline with the Python file.
- **Who hits this:** Any attendee debugging a widget JSON validation failure.

## [P1] Heavy blitz slots risk mid-flight context exhaustion
- **Encountered while:** B4 building the 9-component legal catalog (973 LOC across 4 files)
- **What happened:** The B4 agent's session ended after writing definitions.ts + renderers.tsx + theme.css but before writing index.ts (28 lines) or committing. Files were complete and well-formed — evidence consistent with clean context-window exhaustion at a file boundary. B4-finalize subagent was dispatched to complete the job.
- **Suggested fix:** (a) Decompose heavy slots into smaller ones (defs / renderers / theme / index separately). (b) Document a "resume an interrupted agent" recipe in HACKATHON.md. (c) Pattern: write the cheapest aggregator/index file FIRST or mid-stream, so partial completions still produce a wireable artifact.
- **Who hits this:** Any attendee using Claude Code / Cursor / Gemini CLI for heavy multi-file widget builds.

#!/usr/bin/env node
/**
 * pnpm explain <topic> — Print the right HACKATHON.md section to the terminal.
 *
 * Topics map to HACKATHON.md headings:
 *   themes   → §1 (Re-theme)
 *   branding → §2 (Re-brand the shell)
 *   data     → §3 (Swap demo data)
 *   widgets  → §4 (Add an A2UI component)
 *   domain   → §5 (Swap the agent flow)
 *   a2a      → §6 (BYO A2A agent)
 *
 * If HACKATHON.md is missing (e.g. a trimmed fork), prints a friendly
 * message + the topic-to-section mapping so the hacker still gets a pointer.
 */
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const REPO_ROOT = join(__dirname, "..");
const HACKATHON_MD = join(REPO_ROOT, "HACKATHON.md");

const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";
const CYAN = "\x1b[36m";
const YELLOW = "\x1b[33m";

const TOPIC_TO_SEAM: Record<string, { seam: number; title: string; summary: string }> = {
  themes: {
    seam: 1,
    title: "Re-theme",
    summary:
      "Edit src/a2ui/theme.css (A2UI surface tokens) + src/app/(pdf)/pdf-analyst.css (shell brand tokens). CSS variables, no rebuild. `pnpm theme:reset` reverts.",
  },
  branding: {
    seam: 2,
    title: "Re-brand the shell",
    summary:
      "Edit src/components/pdf-analyst/Brand.tsx (Logo, SiteNav, PageHeader, WorkspaceHeader). Swap the asset in public/brand/. Keeps the layout intact.",
  },
  data: {
    seam: 3,
    title: "Swap demo data",
    summary:
      "The uploaded PDF is the data. Tune the extraction prompt + TypedDict shapes in agent/src/pdf_tools.py, and the agent system prompts in agent/src/fixed_agent.py / dynamic_agent.py.",
  },
  widgets: {
    seam: 4,
    title: "Add an A2UI component",
    summary:
      "Add a definition (Zod props) to src/a2ui/catalog/definitions.ts, a React renderer to src/a2ui/catalog/renderers.tsx, and mirror a one-line summary in agent/src/catalog.py's CATALOG_PROMPT. See HACKATHON.md §4 or `.claude/skills/create-a2ui-widget`.",
  },
  domain: {
    seam: 5,
    title: "Swap the agent flow",
    summary:
      "Edit agent/src/fixed_agent.py (dashboard flow + agent/src/a2ui/schemas/dashboard.json layout) or agent/src/dynamic_agent.py (dynamic Q&A). Both are served by agent/main.py.",
  },
  a2a: {
    seam: 6,
    title: "BYO A2A agent",
    summary:
      "Run `pnpm check-a2a <url>` FIRST. Then set A2A_AGENT_URL in .env. The middleware activates only if the URL is set.",
  },
};

const TOPIC_ALIASES: Record<string, string> = {
  theme: "themes",
  styling: "themes",
  css: "themes",
  brand: "branding",
  header: "branding",
  logo: "branding",
  shell: "branding",
  "demo-data": "data",
  pdf: "data",
  extraction: "data",
  widget: "widgets",
  "a2ui-widget": "widgets",
  card: "widgets",
  component: "widgets",
  catalog: "widgets",
  "fixed-schema": "widgets",
  "dynamic-schema": "widgets",
  agent: "domain",
  agents: "domain",
  flow: "domain",
  "agent-flow": "domain",
  "a2a-agent": "a2a",
  interop: "a2a",
};

function printMapping(): void {
  console.log(`${BOLD}Topics:${RESET}`);
  for (const [key, info] of Object.entries(TOPIC_TO_SEAM)) {
    console.log(`  ${CYAN}${key.padEnd(10)}${RESET} → §${info.seam}: ${info.title}`);
    console.log(`    ${DIM}${info.summary}${RESET}`);
  }
}

/**
 * Extract a seam section from HACKATHON.md. The live headings use the
 * "## §N — Title" form; we also accept the older "## Seam #N" form so the
 * script keeps working if the doc style changes back.
 */
function extractSeamSection(md: string, seamNumber: number): string | null {
  const lines = md.split("\n");
  // Match a heading containing either "§N" or "Seam #N" / "Seam N".
  const startRegex = new RegExp(
    `^(#+)\\s+.*(?:§\\s*${seamNumber}\\b|Seam\\s*#?${seamNumber}\\b)`,
    "i",
  );
  let startIdx = -1;
  let startLevel = 0;

  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(startRegex);
    if (m) {
      startIdx = i;
      startLevel = m[1].length;
      break;
    }
  }
  if (startIdx === -1) return null;

  // Find end: next heading at <= startLevel
  let endIdx = lines.length;
  for (let i = startIdx + 1; i < lines.length; i++) {
    const m = lines[i].match(/^(#+)\s/);
    if (m && m[1].length <= startLevel) {
      endIdx = i;
      break;
    }
  }

  return lines.slice(startIdx, endIdx).join("\n").trim();
}

function main(): void {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log(`${BOLD}pnpm explain <topic>${RESET}\n`);
    printMapping();
    process.exit(0);
  }

  let topicArg = args[0].toLowerCase();
  if (TOPIC_ALIASES[topicArg]) topicArg = TOPIC_ALIASES[topicArg];

  const info = TOPIC_TO_SEAM[topicArg];
  if (!info) {
    console.error(`${YELLOW}Unknown topic:${RESET} ${args[0]}\n`);
    printMapping();
    process.exit(1);
  }

  console.log(`${BOLD}${CYAN}§${info.seam} — ${info.title}${RESET}\n`);
  console.log(`${info.summary}\n`);

  if (!existsSync(HACKATHON_MD)) {
    console.log(`${YELLOW}HACKATHON.md not found in this checkout.${RESET}`);
    console.log(`${DIM}The summary above is still accurate. All seams:${RESET}\n`);
    printMapping();
    process.exit(0);
  }

  const md = readFileSync(HACKATHON_MD, "utf-8");
  const section = extractSeamSection(md, info.seam);
  if (!section) {
    console.log(
      `${YELLOW}HACKATHON.md exists but I couldn't find a heading matching "§${info.seam}".${RESET}`,
    );
    console.log(`${DIM}Run \`grep -n "^##" HACKATHON.md\` to see the actual headings.${RESET}`);
    process.exit(1);
  }

  console.log(section);
  process.exit(0);
}

main();

#!/usr/bin/env node
/**
 * pnpm theme:reset — Revert the Seam #1 theme files to the committed
 * baseline.
 *
 * Baselines live in scripts/theme-baseline/ and are COMMITTED to the repo,
 * so the panic button works on a fresh clone even after you've broken the
 * theme (no first-run snapshot dance — the old behavior could snapshot an
 * already-broken theme as "original").
 *
 * Files restored:
 *   src/a2ui/theme.css             ← scripts/theme-baseline/theme.css
 *   src/app/(pdf)/pdf-analyst.css  ← scripts/theme-baseline/pdf-analyst.css
 *   src/lib/a2ui-theme.css         ← scripts/theme-baseline/a2ui-theme.css
 *
 * If something is too broken to fix manually mid-build, `pnpm theme:reset`
 * is the panic button.
 */
import { copyFileSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const REPO_ROOT = join(__dirname, "..");
const BASELINE_DIR = join(REPO_ROOT, "scripts", "theme-baseline");

// [live path, baseline filename]
const TARGETS: Array<[string, string]> = [
  [join(REPO_ROOT, "src", "a2ui", "theme.css"), "theme.css"],
  [join(REPO_ROOT, "src", "app", "(pdf)", "pdf-analyst.css"), "pdf-analyst.css"],
  [join(REPO_ROOT, "src", "lib", "a2ui-theme.css"), "a2ui-theme.css"],
];

const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

function main(): void {
  let restored = 0;
  let clean = 0;
  let failed = 0;

  for (const [livePath, baselineName] of TARGETS) {
    const baselinePath = join(BASELINE_DIR, baselineName);

    if (!existsSync(baselinePath)) {
      console.error(`${RED}✗${RESET} Baseline missing: ${baselinePath}`);
      console.error(
        `  ${DIM}Restore it from git: git checkout -- scripts/theme-baseline/${RESET}`,
      );
      failed++;
      continue;
    }
    if (!existsSync(livePath)) {
      console.error(`${RED}✗${RESET} Theme file missing: ${livePath}`);
      failed++;
      continue;
    }

    const current = readFileSync(livePath, "utf-8");
    const baseline = readFileSync(baselinePath, "utf-8");
    if (current === baseline) {
      console.log(`${GREEN}✓${RESET} ${DIM}already baseline:${RESET} ${livePath}`);
      clean++;
      continue;
    }

    copyFileSync(baselinePath, livePath);
    console.log(`${GREEN}✓${RESET} restored: ${livePath}`);
    restored++;
  }

  console.log();
  if (failed > 0) {
    console.error(`${RED}${BOLD}Theme reset incomplete${RESET} (${failed} file(s) could not be restored).`);
    process.exit(1);
  }
  if (restored === 0) {
    console.log(`${GREEN}${BOLD}Theme already matches the baseline — nothing to revert.${RESET}`);
  } else {
    console.log(`${GREEN}${BOLD}Theme reset.${RESET} ${DIM}(${restored} restored, ${clean} already clean)${RESET}`);
    console.log(
      `${DIM}If the panic button didn't help, check src/components/pdf-analyst/Brand.tsx${RESET}`,
    );
    console.log(`${DIM}(Seam #2 — re-brand the shell) and src/app/globals.css.${RESET}`);
  }
  process.exit(0);
}

main();

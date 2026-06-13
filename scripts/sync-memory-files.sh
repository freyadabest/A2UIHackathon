#!/usr/bin/env bash
# scripts/sync-memory-files.sh — Re-create CLAUDE.md and GEMINI.md symlinks
# pointing at AGENTS.md. Idempotent.
#
# Why this script exists:
#   - AGENTS.md is the canonical agent guide (cross-tool standard from agents.md).
#   - Claude Code reads CLAUDE.md natively.
#   - Gemini CLI reads GEMINI.md natively.
#   - Both are symlinks to AGENTS.md so we maintain one source of truth.
#   - Windows users who clone the repo via git on certain filesystems lose
#     the symlinks. This script lets them re-create on their machine.
#
# Safe to run repeatedly. Run automatically by Workstream F's postinstall.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_MD="$ROOT/AGENTS.md"

if [[ ! -f "$AGENTS_MD" ]]; then
  echo "WARNING: AGENTS.md not found at $AGENTS_MD" >&2
  echo "  (Workstream C has not landed yet — symlinks will be created when AGENTS.md appears.)" >&2
  exit 0
fi

ensure_symlink() {
  local target="$1" link="$2"
  if [[ -L "$link" ]]; then
    # Already a symlink — verify it points to the right place.
    local current
    current=$(readlink "$link")
    if [[ "$current" == "$target" || "$current" == "$(basename "$target")" ]]; then
      echo "OK: $link → $target (symlink already correct)"
      return 0
    fi
    echo "WARN: $link is a symlink to $current; re-creating to point at $target"
    rm "$link"
  elif [[ -f "$link" ]]; then
    echo "ERROR: $link exists as a regular file (not a symlink)." >&2
    echo "  Refusing to overwrite. Remove $link manually if you want it re-linked." >&2
    return 1
  fi
  # cd into the link's directory so the symlink target is relative.
  ( cd "$(dirname "$link")" && ln -s "$(basename "$target")" "$(basename "$link")" )
  echo "CREATED: $link → $target"
}

ensure_symlink "$AGENTS_MD" "$ROOT/CLAUDE.md"
ensure_symlink "$AGENTS_MD" "$ROOT/GEMINI.md"

echo
echo "Memory files synced."

#!/usr/bin/env bash
# VantageAI — one-command local dev.
# Starts the Python agent (:8000) and the Next.js web app (:3000).
# Works with zero secrets (sample data); set LINKUP_API_KEY in .env for live search.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Load .env if present (LINKUP_API_KEY, GOOGLE_API_KEY, AGENT_URL, ...).
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

cleanup() { kill 0 2>/dev/null || true; }
trap cleanup EXIT INT TERM

echo "→ Starting agent on :8000"
(
  cd services/agent
  if [ ! -d .venv ]; then
    python3 -m venv .venv
    ./.venv/bin/pip install -q --upgrade pip
    ./.venv/bin/pip install -q -r requirements.txt
  fi
  ./.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
) &

echo "→ Starting web on :3000"
(
  cd apps/web
  [ -d node_modules ] || npm install
  AGENT_URL="${AGENT_URL:-http://localhost:8000}" npm run dev
) &

wait

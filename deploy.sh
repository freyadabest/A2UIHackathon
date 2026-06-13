#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# One-shot deploy of Vantage AI to Google Cloud Run.
#
# Easiest path: run this in Google Cloud Shell (gcloud + docker preinstalled,
# already authenticated) from the repo root. Locally it needs the gcloud SDK
# and an authenticated account (`gcloud auth login`).
#
#   ./deploy.sh YOUR_PROJECT_ID
#
# It will (idempotently):
#   1. set the project + enable the required APIs
#   2. create the Artifact Registry repo (if missing)
#   3. create/update the GEMINI_API_KEY + LINKUP_API_KEY secrets
#   4. submit cloudbuild.yaml (build → push → deploy)
#
# Override defaults via env vars:
#   REGION=europe-west2 SERVICE=vantage-ai REPO=vantage-ai ./deploy.sh PROJECT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
set -euo pipefail

PROJECT_ID="${1:-${PROJECT_ID:-}}"
REGION="${REGION:-europe-west2}"
SERVICE="${SERVICE:-vantage-ai}"
REPO="${REPO:-vantage-ai}"

if [[ -z "${PROJECT_ID}" ]]; then
  echo "Usage: ./deploy.sh YOUR_PROJECT_ID  (or set PROJECT_ID env var)" >&2
  exit 1
fi

echo "==> Project: ${PROJECT_ID}  Region: ${REGION}  Service: ${SERVICE}"
gcloud config set project "${PROJECT_ID}" >/dev/null

echo "==> Enabling APIs (run, cloudbuild, artifactregistry, secretmanager)..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com

echo "==> Ensuring Artifact Registry repo '${REPO}' exists..."
if ! gcloud artifacts repositories describe "${REPO}" --location="${REGION}" >/dev/null 2>&1; then
  gcloud artifacts repositories create "${REPO}" \
    --repository-format=docker \
    --location="${REGION}" \
    --description="Vantage AI container images"
fi

# Create or add a new version for each secret. Prompts only if not already in
# the environment (GEMINI_API_KEY / LINKUP_API_KEY).
ensure_secret() {
  local name="$1" value="$2"
  if [[ -z "${value}" ]]; then
    read -r -s -p "Enter ${name}: " value; echo
  fi
  if gcloud secrets describe "${name}" >/dev/null 2>&1; then
    printf '%s' "${value}" | gcloud secrets versions add "${name}" --data-file=-
  else
    printf '%s' "${value}" | gcloud secrets create "${name}" --data-file=-
  fi
}

echo "==> Configuring secrets in Secret Manager..."
ensure_secret GEMINI_API_KEY "${GEMINI_API_KEY:-}"
ensure_secret LINKUP_API_KEY "${LINKUP_API_KEY:-}"

# Let Cloud Run's runtime service account read the secrets.
PROJECT_NUMBER="$(gcloud projects describe "${PROJECT_ID}" --format='value(projectNumber)')"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
for s in GEMINI_API_KEY LINKUP_API_KEY; do
  gcloud secrets add-iam-policy-binding "${s}" \
    --member="serviceAccount:${RUNTIME_SA}" \
    --role="roles/secretmanager.secretAccessor" >/dev/null
done

echo "==> Submitting Cloud Build (build → push → deploy)..."
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions="_REGION=${REGION},_SERVICE=${SERVICE},_REPO=${REPO}"

URL="$(gcloud run services describe "${SERVICE}" --region="${REGION}" --format='value(status.url)')"
echo "==> Deployed: ${URL}"

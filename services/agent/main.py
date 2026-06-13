"""AG-UI server entrypoint for the VantageAI agent (skeleton).

Exposes an HTTP endpoint the CopilotKit runtime connects to. The full AG-UI
event stream wiring lands in Phase 1; this scaffold provides health + a direct
competitor-lookup endpoint for local testing.
"""
import os

from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_competitor_lookup

app = FastAPI(title="VantageAI Agent")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")}


class LookupRequest(BaseModel):
    business_type: str
    area: str


@app.post("/competitors")
def competitors(req: LookupRequest) -> dict:
    """Local dev helper: returns an A2UI panel spec for the competitor table."""
    return run_competitor_lookup(req.business_type, req.area)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

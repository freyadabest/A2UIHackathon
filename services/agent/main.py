"""HTTP server entrypoint for the VantageAI agent.

Exposes the endpoints the frontend uses:
- GET  /health      liveness + active model
- POST /dashboard   one free-text idea -> a generative A2UI dashboard
- POST /competitors direct competitor-table lookup (business_type + area)
"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import build_dashboard, run_competitor_lookup, run_reviews_lookup

app = FastAPI(title="VantageAI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        "linkup": bool(os.environ.get("LINKUP_API_KEY")),
        "gemini": bool(os.environ.get("GOOGLE_API_KEY")),
    }


class DashboardRequest(BaseModel):
    idea: str


@app.post("/dashboard")
def dashboard(req: DashboardRequest) -> dict:
    """Turn one sentence into a generative competitor dashboard."""
    idea = req.idea.strip()
    if not idea:
        raise HTTPException(status_code=400, detail="idea must not be empty")
    try:
        return build_dashboard(idea)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


class LookupRequest(BaseModel):
    business_type: str
    area: str


@app.post("/competitors")
def competitors(req: LookupRequest) -> dict:
    """Direct competitor-table lookup for a known business type + area."""
    try:
        return run_competitor_lookup(req.business_type, req.area)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


class ReviewsRequest(BaseModel):
    competitor: str
    business_type: str
    area: str


@app.post("/reviews")
def reviews(req: ReviewsRequest) -> dict:
    """Analyze reviews for a competitor and return a ReviewThemes panel spec."""
    try:
        return run_reviews_lookup(req.competitor, req.business_type, req.area)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

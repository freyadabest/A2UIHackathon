"""Shared agent tools: live market research via Linkup → structured data.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOMIZATION SEAM #3 — Swap demo data
See HACKATHON.md §3 for the full recipe.

Vantage AI's data is NOT an uploaded PDF — it's the live web. Given a
location + business type ("Pilates studio in Shoreditch"), this module
asks Linkup for a structured competitive landscape (competitors, ratings,
prices, class mix) and returns it as JSON the fixed dashboard binds to.
Edit `_COMPETITOR_SCHEMA` and the query phrasing below to research a
different kind of local business.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from __future__ import annotations

import json
import os
from typing import Any

from langchain.tools import tool

# Linkup is a standalone SDK (does NOT touch the frozen langchain pins). The
# client reads LINKUP_API_KEY from the environment. Imported lazily inside the
# tool so `import main` succeeds with OFFLINE=1 and no Linkup install/key.

# The structured shape we ask Linkup to fill. Linkup's `output_type="structured"`
# returns JSON matching this schema, grounded in live web results — so the
# agent gets clean competitor records instead of prose to parse.
_COMPETITOR_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "competitors": {
                "type": "array",
                "description": "Local competing businesses found near the area.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Business name"},
                        "area": {
                            "type": "string",
                            "description": "Neighbourhood / district, e.g. 'Shoreditch'",
                        },
                        "rating": {
                            "type": "number",
                            "description": "Average star rating out of 5",
                        },
                        "review_count": {
                            "type": "number",
                            "description": "Number of public reviews",
                        },
                        "monthly_price_gbp": {
                            "type": "number",
                            "description": "Approx monthly membership price in GBP",
                        },
                        "offerings": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Class / service types offered",
                        },
                    },
                },
            },
            "summary": {
                "type": "string",
                "description": "One-sentence read on the competitive landscape and the gap for a new entrant.",
            },
        },
    }
)


def _empty_payload(note: str) -> str:
    return json.dumps({"competitors": [], "summary": note, "status": "empty"})


@tool
def research_market(location: str, business_type: str) -> str:
    """Research the live competitive landscape for opening a local business.

    Use this FIRST, once per turn, before rendering the dashboard. It runs a
    live web search (Linkup) and returns a JSON string describing nearby
    competitors and the market gap.

    Args:
        location: The target area, e.g. "Shoreditch" or "Shoreditch, London".
        business_type: The kind of business, e.g. "Pilates studio",
            "specialty coffee shop", "barber".

    Returns a JSON string:
      {
        "competitors": [
          {"name", "area", "rating", "review_count",
           "monthly_price_gbp", "offerings": [..]}
        ],
        "summary": "one-sentence landscape read",
        "status": "ok" | "empty" | "error"
      }
    The agent maps this into render_dashboard. Never invent competitors that
    are not in this result.
    """
    api_key = os.getenv("LINKUP_API_KEY")
    if not api_key:
        return _empty_payload(
            "LINKUP_API_KEY is not set — add a free key from linkup.so to .env "
            "to pull live competitor data."
        )

    try:
        from linkup import LinkupClient
    except ImportError:
        return _empty_payload(
            "linkup-sdk is not installed — run `uv sync` in agent/."
        )

    query = (
        f"Competitor landscape for opening a {business_type} in {location}. "
        f"List the existing {business_type} businesses in and around {location} "
        f"with their average star rating, number of reviews, approximate monthly "
        f"membership price in GBP, and the class or service types they offer. "
        f"Then summarise how saturated the market is and where the gap is for a "
        f"new entrant."
    )

    try:
        client = LinkupClient(api_key=api_key)
        response = client.search(
            query=query,
            depth="standard",
            output_type="structured",
            structured_output_schema=_COMPETITOR_SCHEMA,
        )
    except Exception as exc:  # noqa: BLE001 — degrade, never crash the agent loop
        print(f"[research_market] Linkup search failed: {exc}")
        return _empty_payload(f"Live search failed: {exc}")

    data = _coerce_to_dict(response)
    competitors = data.get("competitors") or []
    if not isinstance(competitors, list):
        competitors = []
    data["competitors"] = competitors
    data.setdefault("summary", "")
    data["status"] = "ok" if competitors else "empty"
    return json.dumps(data)


def _coerce_to_dict(response: Any) -> dict[str, Any]:
    """Linkup may return a pydantic model, a dict, or a JSON string. Normalise."""
    if isinstance(response, dict):
        return response
    if isinstance(response, str):
        try:
            parsed = json.loads(response)
            return parsed if isinstance(parsed, dict) else {"competitors": parsed}
        except json.JSONDecodeError:
            return {"competitors": [], "summary": response}
    # pydantic BaseModel (model_dump) or object with attributes
    for attr in ("model_dump", "dict"):
        fn = getattr(response, attr, None)
        if callable(fn):
            try:
                dumped = fn()
                if isinstance(dumped, dict):
                    return dumped
            except Exception:  # noqa: BLE001
                pass
    structured = getattr(response, "structured", None) or getattr(
        response, "data", None
    )
    if isinstance(structured, dict):
        return structured
    return {"competitors": [], "summary": ""}

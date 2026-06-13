"""VantageAI orchestrator agent (skeleton).

Wires Gemini + tools. The orchestration loop and AG-UI event emission are
stubbed for the scaffold; Phase 1 fills in discover_competitors -> CompetitorTable.
"""
import os

from tools.competitors import discover_competitors
from ui_specs import competitor_table

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Tools the orchestrator can call.
TOOLS = {
    "discover_competitors": discover_competitors,
}


def run_competitor_lookup(business_type: str, area: str) -> dict:
    """Phase 1 happy path: discover competitors and build the panel spec."""
    data = discover_competitors(business_type=business_type, area=area)
    competitors = data.get("competitors", []) if isinstance(data, dict) else []
    return competitor_table(competitors)

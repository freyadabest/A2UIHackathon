"""VantageAI orchestrator agent.

Happy path: a free-text business idea -> parse into (business_type, area) ->
discover competitors via Linkup -> generatively assemble an A2UI dashboard of
panels the frontend renders.

The agent degrades gracefully: without GOOGLE_API_KEY it parses ideas with a
heuristic, and without LINKUP_API_KEY it serves a deterministic sample so the
app still runs and demos.
"""
import os

from tools.competitors import discover_competitors
from tools.idea_parser import parse_idea
from tools.review_analyzer import analyze_reviews
from ui_specs import competitor_table, market_summary, ratings_chart, review_themes_panel

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Tools the orchestrator can call.
TOOLS = {
    "discover_competitors": discover_competitors,
    "parse_idea": parse_idea,
    "analyze_reviews": analyze_reviews,
}

# Used only when LINKUP_API_KEY is absent, so the app demos out of the box.
_SAMPLE = [
    {"name": "Bootcamp Pilates", "rating": 4.6, "reviews": 500, "location": "Shoreditch, London", "url": "https://example.com"},
    {"name": "BLOK Shoreditch", "rating": 4.6, "reviews": 480, "location": "Principal Place, Shoreditch", "url": "https://example.com"},
    {"name": "Stretch London", "rating": 4.5, "reviews": 151, "location": "Shoreditch, London", "url": "https://example.com"},
    {"name": "Hoxton Pilates", "rating": 4.4, "reviews": 96, "location": "Hoxton, London", "url": "https://example.com"},
    {"name": "Tempo Pilates", "rating": 4.2, "reviews": 64, "location": "Shoreditch, London", "url": "https://example.com"},
]


def _competitors_for(business_type: str, area: str) -> list[dict]:
    if not os.environ.get("LINKUP_API_KEY"):
        return _SAMPLE
    data = discover_competitors(business_type=business_type, area=area)
    competitors = data.get("competitors", []) if isinstance(data, dict) else []
    return [c for c in competitors if isinstance(c, dict) and c.get("name")]


def run_competitor_lookup(business_type: str, area: str) -> dict:
    """Discover competitors and build the competitor-table panel spec."""
    competitors = _competitors_for(business_type, area)
    return competitor_table(competitors)


def run_reviews_lookup(competitor_name: str, business_type: str, area: str) -> dict:
    """Analyze reviews for a competitor and build the review-themes panel spec."""
    result = analyze_reviews(competitor_name, business_type, area)
    return review_themes_panel(result)


def build_dashboard(idea: str) -> dict:
    """One sentence in -> a full generative A2UI dashboard out."""
    business_type, area = parse_idea(idea)
    competitors = _competitors_for(business_type, area)

    panels = [
        market_summary(business_type, area, competitors),
        ratings_chart(competitors),
        competitor_table(competitors),
    ]
    return {
        "idea": idea,
        "businessType": business_type,
        "area": area,
        "usingSampleData": not os.environ.get("LINKUP_API_KEY"),
        "panels": panels,
    }

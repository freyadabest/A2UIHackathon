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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# analyze_reviews — competitor "deep dive": strength/weakness review themes.
#
# Ported from the deepdive branch (services/agent/tools/review_analyzer.py)
# onto main's tool conventions: a @tool returning a JSON string, lazy SDK
# imports (so `import main` works under OFFLINE=1), GEMINI_API_KEY + MODEL
# env, and graceful degradation to sample data when keys are missing.
# Pairs with the ReviewThemes catalog component (see src/a2ui/catalog).
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Deterministic fallback so the deep-dive demos out of the box without keys.
_SAMPLE_THEMES: dict[str, list[dict[str, Any]]] = {
    "strengths": [
        {
            "theme": "Great amenities & facilities",
            "mentions": 12,
            "sentiment": "positive",
            "examples": [
                "Love the modern equipment and clean changing rooms",
                "Best studio in the area, amazing showers and towels",
            ],
        },
        {
            "theme": "Friendly & knowledgeable instructors",
            "mentions": 8,
            "sentiment": "positive",
            "examples": [
                "Sarah really knows her stuff and makes classes fun",
                "Instructors are super welcoming to beginners",
            ],
        },
    ],
    "weaknesses": [
        {
            "theme": "No air conditioning",
            "mentions": 6,
            "sentiment": "negative",
            "examples": [
                "Class was great but room was boiling hot",
                "Please install AC, summer classes are unbearable",
            ],
        },
        {
            "theme": "Limited class availability",
            "mentions": 4,
            "sentiment": "negative",
            "examples": [
                "Evening slots always fully booked",
                "Would love more weekend morning classes",
            ],
        },
    ],
}


def _sample_payload(competitor_name: str) -> str:
    return json.dumps(
        {
            "competitor": competitor_name,
            "usingSampleData": True,
            **_SAMPLE_THEMES,
        }
    )


def _search_reviews(competitor_name: str, business_type: str, area: str) -> str:
    """Pull review prose for one competitor via Linkup. Returns "" on failure."""
    try:
        from linkup import LinkupClient
    except ImportError:
        return ""

    query = (
        f'"{competitor_name}" {business_type} {area} customer reviews. '
        f"Summarise what reviewers repeatedly praise and complain about."
    )
    try:
        client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))
        result = client.search(
            query=query, depth="standard", output_type="sourcedAnswer"
        )
    except Exception as exc:  # noqa: BLE001 — degrade, never crash the loop
        print(f"[analyze_reviews] Linkup search failed: {exc}")
        return ""

    if isinstance(result, dict):
        return result.get("answer", "") or ""
    answer = getattr(result, "answer", None)
    return answer if isinstance(answer, str) else ""


def _extract_themes(review_text: str) -> dict[str, list[dict[str, Any]]]:
    """Use Gemini to extract strength/weakness themes. Falls back to sample."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        return _SAMPLE_THEMES

    prompt = f"""Analyze the following customer reviews and extract the most
frequently-mentioned themes.

For each theme provide:
- theme: a short label (1-5 words)
- mentions: estimated number of times mentioned (integer)
- sentiment: "positive" or "negative"
- examples: 1-2 exact quotes that illustrate the theme

Group themes into "strengths" (positive) and "weaknesses" (negative). Only
include themes mentioned at least 3 times.

Reviews:
{review_text[:4000]}

Respond ONLY with valid JSON of shape:
{{"strengths": [{{"theme": "...", "mentions": 5, "sentiment": "positive",
"examples": ["..."]}}], "weaknesses": [{{"theme": "...", "mentions": 3,
"sentiment": "negative", "examples": ["..."]}}]}}
"""
    try:
        model = ChatGoogleGenerativeAI(
            model=os.getenv("MODEL", "gemini-3.5-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0,
        )
        text = str(model.invoke(prompt).content).strip()
        if text.startswith("```"):
            # strip ```json / ``` fences
            text = text.split("\n", 1)[-1] if "\n" in text else text
            text = text.removeprefix("json").strip()
            if text.endswith("```"):
                text = text[:-3].strip()
        parsed = json.loads(text)
        return {
            "strengths": parsed.get("strengths", []),
            "weaknesses": parsed.get("weaknesses", []),
        }
    except Exception as exc:  # noqa: BLE001
        print(f"[analyze_reviews] theme extraction failed: {exc}")
        return _SAMPLE_THEMES


@tool
def analyze_reviews(competitor_name: str, business_type: str, area: str) -> str:
    """Deep-dive ONE competitor's customer reviews into strength/weakness themes.

    Use this when the user wants to drill into a single competitor's reviews
    (e.g. "what do reviewers love/hate about BLOK Shoreditch?"). Pair the
    result with the ReviewThemes component via render_review_themes.

    Args:
        competitor_name: The specific business to analyse, e.g. "BLOK Shoreditch".
        business_type: The kind of business, e.g. "Pilates studio".
        area: The neighbourhood / city, e.g. "Shoreditch, London".

    Returns a JSON string:
      {
        "competitor": str,
        "usingSampleData": bool,
        "strengths":  [{"theme","mentions","sentiment","examples":[str]}],
        "weaknesses": [{"theme","mentions","sentiment","examples":[str]}]
      }
    Degrades to representative sample themes when LINKUP_API_KEY or
    GEMINI_API_KEY is missing, or when the live search/extraction fails.
    """
    if not os.getenv("LINKUP_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        return _sample_payload(competitor_name)

    review_text = _search_reviews(competitor_name, business_type, area)
    if not review_text:
        return _sample_payload(competitor_name)

    themes = _extract_themes(review_text)
    # _extract_themes returns _SAMPLE_THEMES on failure — flag that honestly.
    is_sample = themes is _SAMPLE_THEMES
    return json.dumps(
        {
            "competitor": competitor_name,
            "usingSampleData": is_sample,
            **themes,
        }
    )


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

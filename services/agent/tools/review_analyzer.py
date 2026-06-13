"""analyze_reviews — extract strengths & weaknesses themes from Google reviews.

Searches for reviews of a named competitor, then uses Gemini to extract
repeatedly-mentioned themes (e.g. "great amenities" in 5-star reviews,
"no air conditioning" in 1-star reviews).
"""
import json
import os
from typing import Any

from tools.linkup_client import search

# Fallback sample when no keys are available
_SAMPLE_THEMES = {
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


def _search_reviews(competitor_name: str, business_type: str, area: str) -> str:
    """Search for reviews of a specific competitor. Returns raw text."""
    query = f'"{competitor_name}" {business_type} {area} reviews Google'
    try:
        result = search(query=query, depth="standard", output_type="sourcedAnswer")
    except TimeoutError:
        return ""

    # SourcedAnswer returns { answer: str, sources: [...] }
    if isinstance(result, dict):
        return result.get("answer", "") or ""
    return ""


def _extract_themes_with_gemini(review_text: str) -> dict[str, list[dict[str, Any]]]:
    """Use Gemini to extract strength/weakness themes from review text."""
    try:
        from google import genai
    except ImportError:
        return _SAMPLE_THEMES

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    prompt = f"""Analyze the following customer reviews and extract the most
frequently-mentioned themes.

For each theme, provide:
- theme: a short label (1-5 words)
- mentions: estimated number of times mentioned
- sentiment: "positive" or "negative"
- examples: 1-2 exact quotes that illustrate the theme

Group themes into "strengths" (positive) and "weaknesses" (negative).
Only include themes that are mentioned at least 3 times.

Reviews:
{review_text[:4000]}

Respond ONLY with valid JSON in this exact shape:
{{
  "strengths": [
    {{
      "theme": "...",
      "mentions": 5,
      "sentiment": "positive",
      "examples": ["...", "..."]
    }}
  ],
  "weaknesses": [
    {{
      "theme": "...",
      "mentions": 3,
      "sentiment": "negative",
      "examples": ["...", "..."]
    }}
  ]
}}
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        text = response.text or ""
        # Strip markdown code fences if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        parsed = json.loads(text)
        return {
            "strengths": parsed.get("strengths", []),
            "weaknesses": parsed.get("weaknesses", []),
        }
    except Exception:
        return _SAMPLE_THEMES


def analyze_reviews(competitor_name: str, business_type: str, area: str) -> dict:
    """Return strength/weakness themes extracted from Google reviews.

    Falls back to sample data when API keys are missing.
    """
    if not os.environ.get("LINKUP_API_KEY") or not os.environ.get("GOOGLE_API_KEY"):
        return {
            "competitor": competitor_name,
            "usingSampleData": True,
            **_SAMPLE_THEMES,
        }

    review_text = _search_reviews(competitor_name, business_type, area)
    if not review_text:
        return {
            "competitor": competitor_name,
            "usingSampleData": True,
            **_SAMPLE_THEMES,
        }

    themes = _extract_themes_with_gemini(review_text)
    # If Gemini failed, _extract_themes_with_gemini returns _SAMPLE_THEMES.
    # Detect that and set the flag correctly.
    is_sample = (
        len(themes.get("strengths", [])) == len(_SAMPLE_THEMES["strengths"])
        and themes["strengths"][0]["theme"] == _SAMPLE_THEMES["strengths"][0]["theme"]
    )
    return {
        "competitor": competitor_name,
        "usingSampleData": is_sample,
        **themes,
    }

"""Turn a free-text business idea into (business_type, area).

Uses Gemini when GOOGLE_API_KEY is set; otherwise falls back to a lightweight
heuristic so the agent runs and demos with zero extra secrets.
"""
import os
import re

_LOCATION_PREPS = ("in", "near", "around", "at", "within")
_STOPWORDS = {
    "i", "want", "to", "open", "start", "launch", "a", "an", "the", "my",
    "new", "build", "run", "create", "set", "up", "some", "kind", "of",
    "business", "shop", "store", "thinking", "about", "would", "like",
    "planning", "plan",
}


def _heuristic(idea: str) -> tuple[str, str]:
    text = idea.strip().rstrip(".").strip()
    area = ""
    business = text

    # Split on the last location preposition, e.g. "... studio in Shoreditch".
    pattern = r"\b(" + "|".join(_LOCATION_PREPS) + r")\b"
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
    if matches:
        last = matches[-1]
        business = text[: last.start()].strip()
        area = text[last.end():].strip()

    # Clean the business phrase of leading intent words.
    tokens = re.split(r"\s+", business)
    while tokens and tokens[0].lower() in _STOPWORDS:
        tokens.pop(0)
    business = " ".join(tokens).strip() or text

    return business or "local business", area or "London"


def _gemini(idea: str) -> tuple[str, str] | None:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        prompt = (
            "Extract the business type and the geographic area from this idea. "
            'Respond as strict JSON: {"business_type": "...", "area": "..."}.\n'
            f"Idea: {idea}"
        )
        resp = client.models.generate_content(model=model, contents=prompt)
        raw = (resp.text or "").strip()
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            return None
        import json

        data = json.loads(match.group(0))
        business = str(data.get("business_type", "")).strip()
        area = str(data.get("area", "")).strip()
        if business and area:
            return business, area
    except Exception:
        return None
    return None


def parse_idea(idea: str) -> tuple[str, str]:
    """Return (business_type, area) for a free-text business idea."""
    return _gemini(idea) or _heuristic(idea)

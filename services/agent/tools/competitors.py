"""discover_competitors — find local competitors via Linkup."""
import json

from tools.linkup_client import search

COMPETITOR_SCHEMA = {
    "type": "object",
    "properties": {
        "competitors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "rating": {"type": "number"},
                    "reviews": {"type": "integer"},
                    "url": {"type": "string"},
                    "location": {"type": "string"},
                },
                "required": ["name"],
            },
        }
    },
    "required": ["competitors"],
}


def _competitors(result: object) -> list:
    if isinstance(result, dict):
        return result.get("competitors", []) or []
    return []


def _try_search(query: str, depth: str, schema: str) -> list:
    """Run one structured search, returning [] on timeout instead of hanging."""
    try:
        result = search(
            query=query,
            depth=depth,
            output_type="structured",
            structured_output_schema=schema,
        )
    except TimeoutError:
        return []
    return _competitors(result)


def discover_competitors(business_type: str, area: str) -> dict:
    """Return a structured list of competing businesses in an area.

    Linkup's structured search can return an empty set for some phrasings, so we
    retry once at greater depth before giving up. Each call is time-bounded so a
    slow upstream search can't hang the request.
    """
    schema = json.dumps(COMPETITOR_SCHEMA)
    primary = (
        f"best rated {business_type}s in {area}, "
        "list each with its star rating (out of 5) and number of reviews"
    )
    alt = f"top {business_type}s in {area} with their Google rating and review count"

    # Two fast standard attempts (different phrasings) before the slow deep pass.
    competitors = _try_search(primary, "standard", schema)
    if not competitors:
        competitors = _try_search(alt, "standard", schema)
    if not competitors:
        competitors = _try_search(primary, "deep", schema)

    return {"competitors": competitors}

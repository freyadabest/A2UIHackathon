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


def discover_competitors(business_type: str, area: str) -> dict:
    """Return a structured list of competing businesses in an area.

    Linkup's structured search can return an empty set for some phrasings, so we
    retry once at greater depth before giving up.
    """
    query = (
        f"best rated {business_type}s in {area}, "
        "list each with its star rating (out of 5) and number of reviews"
    )
    schema = json.dumps(COMPETITOR_SCHEMA)

    result = search(
        query=query,
        depth="standard",
        output_type="structured",
        structured_output_schema=schema,
    )
    competitors = _competitors(result)
    if not competitors:
        result = search(
            query=query,
            depth="deep",
            output_type="structured",
            structured_output_schema=schema,
        )
        competitors = _competitors(result)

    return {"competitors": competitors}

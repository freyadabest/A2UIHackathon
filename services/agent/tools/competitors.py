"""discover_competitors — find local competitors via Linkup."""
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


def discover_competitors(business_type: str, area: str) -> dict:
    """Return a structured list of competing businesses in an area."""
    query = f"{business_type} studios and competitors in {area}, with ratings and review counts"
    result = search(
        query=query,
        depth="standard",
        output_type="structured",
        structured_output_schema=COMPETITOR_SCHEMA,
    )
    return result

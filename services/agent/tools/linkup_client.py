"""Thin Linkup wrapper with Redis caching."""
import os
from typing import Any

from linkup import LinkupClient

from cache import get_cached, set_cached

_client = LinkupClient(api_key=os.environ.get("LINKUP_API_KEY", ""))


def search(query: str, depth: str = "standard", output_type: str = "searchResults", **kwargs: Any):
    """Run a Linkup search, caching the result in Redis."""
    payload = {"query": query, "depth": depth, "output_type": output_type, **kwargs}
    cached = get_cached("linkup", payload)
    if cached is not None:
        return cached

    result = _client.search(
        query=query,
        depth=depth,
        output_type=output_type,
        **kwargs,
    )
    # SDK returns a pydantic-ish object; normalise to dict for caching.
    value = result.model_dump() if hasattr(result, "model_dump") else result
    set_cached("linkup", payload, value)
    return value

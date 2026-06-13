"""Thin Linkup wrapper with Redis caching."""
import os
from typing import Any

from linkup import LinkupClient

from cache import get_cached, set_cached

_client: LinkupClient | None = None


def _get_client() -> LinkupClient:
    """Lazily build the Linkup client so the service can boot without a key."""
    global _client
    if _client is None:
        api_key = os.environ.get("LINKUP_API_KEY")
        if not api_key:
            raise RuntimeError("LINKUP_API_KEY is not set")
        _client = LinkupClient(api_key=api_key)
    return _client


def search(query: str, depth: str = "standard", output_type: str = "searchResults", **kwargs: Any):
    """Run a Linkup search, caching the result in Redis."""
    payload = {"query": query, "depth": depth, "output_type": output_type, **kwargs}
    cached = get_cached("linkup", payload)
    if cached is not None:
        return cached

    result = _get_client().search(
        query=query,
        depth=depth,
        output_type=output_type,
        **kwargs,
    )
    # SDK returns a pydantic-ish object; normalise to dict for caching.
    value = result.model_dump() if hasattr(result, "model_dump") else result
    set_cached("linkup", payload, value)
    return value

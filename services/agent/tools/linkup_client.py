"""Thin Linkup wrapper with Redis caching and a bounded per-call timeout."""
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Any

from linkup import LinkupClient

from cache import get_cached, set_cached

# Per-call wall-clock budget. Linkup (especially depth="deep") can occasionally
# stall for a minute+; without this the request hangs the whole UI.
SEARCH_TIMEOUT = float(os.environ.get("LINKUP_TIMEOUT", "20"))

_client: LinkupClient | None = None
_executor = ThreadPoolExecutor(max_workers=4)


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
    """Run a Linkup search (cached, time-bounded).

    Raises TimeoutError if the call exceeds SEARCH_TIMEOUT so callers can fall
    back instead of hanging.
    """
    payload = {"query": query, "depth": depth, "output_type": output_type, **kwargs}
    cached = get_cached("linkup", payload)
    if cached is not None:
        return cached

    future = _executor.submit(
        _get_client().search,
        query=query,
        depth=depth,
        output_type=output_type,
        **kwargs,
    )
    try:
        result = future.result(timeout=SEARCH_TIMEOUT)
    except FutureTimeout as exc:
        raise TimeoutError(f"Linkup search timed out after {SEARCH_TIMEOUT}s") from exc

    # SDK returns a pydantic-ish object; normalise to dict for caching.
    value = result.model_dump() if hasattr(result, "model_dump") else result
    set_cached("linkup", payload, value)
    return value

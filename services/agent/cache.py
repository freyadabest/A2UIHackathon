"""Redis helpers: response cache + shared state.

Caching is best-effort. If the `redis` package is missing or the server is
unreachable, every helper degrades to a no-op so the agent still runs locally
with zero infrastructure.
"""
import hashlib
import json
import os
from typing import Any, Optional

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
DEFAULT_TTL = 60 * 60  # 1 hour

try:
    import redis

    _client = redis.from_url(REDIS_URL, decode_responses=True)
    _RedisError = redis.RedisError
except Exception:  # package missing or bad URL — caching disabled
    redis = None  # type: ignore[assignment]
    _client = None
    _RedisError = Exception


def _key(namespace: str, payload: dict) -> str:
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return f"vantageai:{namespace}:{digest}"


def get_cached(namespace: str, payload: dict) -> Optional[Any]:
    if _client is None:
        return None
    try:
        raw = _client.get(_key(namespace, payload))
    except _RedisError:
        return None  # degrade gracefully if Redis is unavailable
    return json.loads(raw) if raw else None


def set_cached(namespace: str, payload: dict, value: Any, ttl: int = DEFAULT_TTL) -> None:
    if _client is None:
        return
    try:
        _client.set(_key(namespace, payload), json.dumps(value), ex=ttl)
    except _RedisError:
        pass  # caching is best-effort

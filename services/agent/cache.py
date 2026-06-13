"""Redis helpers: response cache, shared state, (vector cache TODO)."""
import hashlib
import json
import os
from typing import Any, Optional

import redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
_client = redis.from_url(REDIS_URL, decode_responses=True)

DEFAULT_TTL = 60 * 60  # 1 hour


def _key(namespace: str, payload: dict) -> str:
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return f"vantageai:{namespace}:{digest}"


def get_cached(namespace: str, payload: dict) -> Optional[Any]:
    try:
        raw = _client.get(_key(namespace, payload))
    except redis.RedisError:
        return None  # degrade gracefully if Redis is unavailable
    return json.loads(raw) if raw else None


def set_cached(namespace: str, payload: dict, value: Any, ttl: int = DEFAULT_TTL) -> None:
    try:
        _client.set(_key(namespace, payload), json.dumps(value), ex=ttl)
    except redis.RedisError:
        pass  # caching is best-effort

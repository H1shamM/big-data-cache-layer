import os
import time
import redis
from prometheus_client import Counter, Histogram

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB, decode_responses=True
)

CACHE_HIT_COUNTER = Counter(
    "cache_hits_total",
    "Total number of cache hits"
)
CACHE_MISS_COUNTER = Counter(
    "cache_misses_total",
    "Total number of cache misses"
)
REQUEST_LATENCY_HIST = Histogram(
    "request_latency_seconds",
    "Histogram of request processing time (sec)"
)


def get_from_cache(key: str):
    """Attempt to fetch value from Redis. If found, increment hit counter."""
    value = r.get(key)
    if value is not None:
        CACHE_HIT_COUNTER.inc()
    else:
        CACHE_MISS_COUNTER.inc()

    return value


def set_in_cache(key: str, value: str, ttl: int = 60):
    """Store value in Redis with a TTL (default: 60 seconds)."""
    ttl_s = int(os.getenv("REDIS_TTL", str(ttl)))
    r.set(key, value, ex=ttl_s)


def fetch_from_source(key: str):
    """
    Simulate slow origin; in milliseconds via ORIGIN_LATENCY_MS (default 200ms)
    """
    delay_ms = int(os.getenv("ORIGIN_LATENCY_MS", "200"))
    time.sleep(delay_ms / 1000.0)
    return f"value_for_{key}"

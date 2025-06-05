import os
import time
import redis
from prometheus_client import Counter, Histogram

REDIS_HOST  = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT  = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB    = int(os.getenv("REDIS_DB","0"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

CACHE_HIT_COUNTER   = Counter("cache_hits_total", "Total number of cache hits")
CACHE_MISS_COUNTER  = Counter("cache_misses_total", "Total number of cache misses")
REQUEST_LATENCY_HIST = Histogram("request_latency_seconds", "Histogram of request processing time (sec)")

def get_from_cache(key: str):
    """Attempt to fetch value from Redis. If found, increment hit counter."""
    value = r.get(key)
    if value is not None:
        CACHE_HIT_COUNTER.inc()

    return value

def set_in_cache(key: str, value: str, ttl: int = 60):
    """Store value in Redis with a TTL (default: 60 seconds)."""
    r.set(key, value, ex=ttl)

def fetch_from_source(key: str):
    """
    Simulate a slow data source. Replace it with real DB call in production.
    Here, we just wait 0.2 seconds and return a dummy value.
    """
    time.sleep(0.2)  # simulate latency
    return f"value_for_{key}"


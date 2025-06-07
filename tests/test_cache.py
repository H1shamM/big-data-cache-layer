import pytest
import time
from fakeredis import FakeStrictRedis
from prometheus_client import CollectorRegistry

import app.cache as cache_module

@pytest.fixture(autouse=True)
def use_fakeredis(monkeypatch):
    fake_redis = FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr(cache_module,'r',fake_redis)

    registry = CollectorRegistry()
    monkeypatch.setattr("app.cache.CACHE_HIT_COUNTER", cache_module.Counter(
        "cache_hits_total_test", "Test cache hits", registry=registry))
    monkeypatch.setattr("app.cache.CACHE_MISS_COUNTER", cache_module.Counter(
        "cache_misses_total_test", "Test cache misses", registry=registry))
    monkeypatch.setattr("app.cache.REQUEST_LATENCY_HIST", cache_module.Histogram(
        "request_latency_seconds_test", "Test latency histogram", registry=registry))
    yield

def test_cache_miss_then_hit():
    key = "testkey"

    assert cache_module.get_from_cache(key) is None

    value = cache_module.fetch_from_source(key)
    assert value == f"value_for_{key}"
    cache_module.set_in_cache(key,value,ttl=1)

    cached_value = cache_module.get_from_cache(key)
    assert cached_value == value

    time.sleep(1.1)
    assert cache_module.get_from_cache(key) is None

def test_cache_hit_counter_and_miss_counter():
    key = "abc"

    assert cache_module.r.get(key) is None

    _ = cache_module.get_from_cache(key)

    cache_module.set_in_cache(key, "someval")
    _ = cache_module.get_from_cache(key)

    metric_samples = cache_module.CACHE_HIT_COUNTER.collect()[0].samples
    assert any(sample.value == 1 for sample in metric_samples)


def test_latency_histogram_records_time(monkeypatch):
    start = time.perf_counter()
    monkeypatch.setattr(cache_module,"fetch_from_source", lambda x:"dummy")

    key = "xyz"

    with cache_module.REQUEST_LATENCY_HIST.time():
        _ = cache_module.fetch_from_source(key)

    hist = cache_module.REQUEST_LATENCY_HIST.collect()[0]

    samples = [s for s in hist.samples if s.name.endswith("_count")]
    assert len(samples) == 1
    assert samples[0].value == 1
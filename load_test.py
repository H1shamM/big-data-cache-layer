import time

import requests
from statistics import mean, median

BASE_URL = "http://localhost:5000/items"
TOTAL_REQUESTS = 50
CACHE_KEY = "foo"
UNIQUE_KEYS = [f"k{i}" for i in range(10)]

def single_request(key: str):
    """Send one GET request to /items/{key}, return (latency, source)."""
    url = f"{BASE_URL}/{key}"
    start = time.perf_counter()
    resp = requests.get(url, timeout=5)
    elapsed = time.perf_counter() -start

    try:
        data = resp.json()
        source = data.get("source", "unknown")
    except Exception:
        source = "error"

    return elapsed, source

def run_test():
    latencies = []
    sources = {"cache": 0 ,"origin": 0, "error": 0}

    for i in range(TOTAL_REQUESTS):
        if i < int(TOTAL_REQUESTS * 0.7):
            key = CACHE_KEY
        else:
            key = UNIQUE_KEYS[i % len(UNIQUE_KEYS)]

        latency, source = single_request(key)

        latencies.append(latency)
        sources[source] = sources.get(source, 0) + 1

        print(f"[{i+1}/{TOTAL_REQUESTS}] key={key} | {source.upper():6} | {latency*1000:6.2f} ms")

    avg = mean(latencies)
    med = median(latencies)
    hit_rate = sources["cache"] / (sources["cache"] + sources["origin"]) if (sources["cache"] + sources["origin"]) else 0

    print("\n=== Summary ===")
    print(f"Total requests:  {TOTAL_REQUESTS}")
    print(f"Cache hits:      {sources['cache']}")
    print(f"Cache misses:    {sources['origin']}")
    print(f"Errors:          {sources['error']}")
    print(f"Cache‐hit rate:  {hit_rate * 100:5.2f}%")
    print(f"Avg latency:     {avg * 1000:6.2f} ms")
    print(f"Median latency:  {med * 1000:6.2f} ms")

if __name__ == "__main__":
    run_test()
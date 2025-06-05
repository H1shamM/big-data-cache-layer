# Big-Data Cache Layer

**Overview**  
This project implements a simple Big-Data cache layer using FastAPI and Redis. It demonstrates:
- In-memory caching patterns with Redis.
- Performance improvements via caching.
- Metrics instrumentation with Prometheus.
- Dockerized setup with `docker-compose` for easy deployment.

---

## Prerequisites

- **Docker & Docker Compose**: To run Redis and FastAPI services.
- **Python 3.11+**: For local development and running load tests.
- **pip**: To install Python dependencies if running locally.
- **Git**: To manage the repository.

---

## Project Layout

```
big-data-cache-layer/
├── app/
│   ├── cache.py           # Redis client and Prometheus metrics
│   └── main.py            # FastAPI application
├── Dockerfile             # Builds FastAPI container
├── docker-compose.yml     # Defines Redis and FastAPI services
├── load_test.py           # Script to benchmark cache performance
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation (this file)
```

---

## Setup & Run

### 1. Clone Repository (once created)
```bash
git clone https://github.com/H1shamM/big-data-cache-layer.git
cd big-data-cache-layer
```

### 2. Build and Start Services with Docker Compose
```bash
docker-compose up --build -d
```
- **Redis** will be available at `redis:6379` inside the Docker network.
- **FastAPI** will run on `http://localhost:5000`.

### 3. Verify Endpoints
- **Cache Endpoint**:  
  ```bash
  curl http://localhost:5000/items/foo
  ```
  - First call: cache miss → simulated origin fetch (~200ms).  
  - Second call: cache hit → fast response (~10–20ms).

- **Metrics Endpoint**:  
  ```bash
  curl http://localhost:5000/metrics
  ```
  - Exposes Prometheus metrics: `cache_hits_total`, `cache_misses_total`, and `request_latency_seconds`.

---

## Load Testing & Benchmarking

We measure cache performance using `load_test.py`, which sends 50 requests:
- 70% for the same key (`foo`) → intended cache hits after initial fetch.
- 30% for unique keys (`k0`, `k1`, …) → forced cache misses.

**Sample Results** (on a local machine with Redis + FastAPI in Docker):

```
=== Summary ===
Total requests:   50
Cache hits:       39
Cache misses:     11
Errors:           0
Cache‐hit rate:   78.00%
Avg latency:      66.02 ms
Median latency:   17.55 ms
```

- **Cache‐hit rate**: 78% (most requests served from Redis in ~10–20 ms).  
- **Cache‐misses**: Take ~200 ms (simulated “slow” origin).  
- **Avg latency**: 66 ms (mixed hits and misses).  
- **Median latency**: 17 ms (cache‐dominant).

To reproduce these results:
```bash
# 1. Ensure Docker Compose is running
docker-compose up -d

# 2. Run the load-test script
python load_test.py

# 3. Observe per-request output and summary above
```

---

## Cleanup

To stop and remove containers:
```bash
docker-compose down
```


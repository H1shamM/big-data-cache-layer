# Big-Data Cache Layer

**Overview**  
This project implements a simple Big-Data cache layer using FastAPI and Redis. It demonstrates:
- In-memory caching patterns with Redis.
- Performance improvements via caching.
- Metrics instrumentation with Prometheus.
- Visualization with Grafana dashboards.
- Containerized setup with Docker Compose for easy deployment.

---

## Prerequisites

- **Docker** (with Compose plugin) to build and run containers.
- **Python 3.11+** for local development and load testing.
- **pip** to install Python dependencies locally.
- **Git** to clone and manage the repo.

---

## Project Layout

```
big-data-cache-layer/
├── app/
│   ├── cache.py           # Redis client, configurable TTL & latency, Prometheus metrics
│   └── main.py            # FastAPI application with health & metrics endpoints
├── grafana/               # Grafana provisioning: data source & dashboards
│   ├── datasource/prometheus.yaml
│   └── dashboards/cache-metrics.json
├── prometheus.yml         # Prometheus scrape configuration
├── Dockerfile             # Builds FastAPI container (Python 3.11 slim)
├── docker-compose.yml     # Defines Redis, FastAPI, Prometheus, Grafana services
├── load_test.py           # Benchmarks cache performance and prints summary
├── tests/                 # Unit tests for caching logic using pytest + fakeredis
│   └── test_cache.py
├── requirements.txt       # Pinned Python dependencies
├── .github/workflows/ci.yml  # GitHub Actions: CI, tests, lint, and smoke test
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
docker compose up --build -d
```
- **Redis**: available at `redis:6379` in Docker network.  
- **FastAPI**: HTTP on `http://localhost:5000`.  
- **Prometheus**: UI at `http://localhost:9090`.  
- **Grafana**: UI at `http://localhost:3000` (admin/admin).

### 3. Verify Endpoints
- **Cache Endpoint**:  
  ```bash
  curl http://localhost:5000/items/foo
  ```
  - First call: cache miss → simulated origin (~200 ms).  
  - Second call: cache hit → fast (~10–20 ms).

- **Metrics Endpoint**:  
  ```bash
  curl http://localhost:5000/metrics
  ```
  - Shows Prometheus metrics: `cache_hits_total`, `cache_misses_total`, `request_latency_seconds`.

- **Health Endpoint**:  
  ```bash
  curl http://localhost:5000/health
  ```
  - Returns `{"status":"ok"}` if Redis is reachable.

---

## Configuration

All key parameters can be set via environment variables (in `docker-compose.yml` or your shell):

- `REDIS_TTL` (seconds): cache time-to-live (default `300`).  
- `ORIGIN_LATENCY_MS`: simulated origin latency in ms (default `200`).

---

## Load Testing & Benchmarking

Run the benchmark script:

```bash
python load_test.py
```

By default, it sends 50 requests (70% to the same key, 30% to unique keys) and prints a summary like:

```
=== Summary ===
Total requests:   50
Cache hits:       39
Cache misses:     11
Errors:           0
Cache-hit rate:   78.00%
Avg latency:      66.02 ms
Median latency:   17.55 ms
```

---

## Unit Tests

Run tests with `pytest`:

```bash
pytest -q
```
- Uses `fakeredis` for in-memory Redis mocking.  
- Verifies cache hit/miss counters and latency histogram.

---

## Continuous Integration

CI is configured in `.github/workflows/ci.yml` to:

1. Run `pytest` and `flake8`.  
2. Build Docker images via `docker compose`.  
3. Smoke-test the API using the `/health` endpoint.

---

## Cleanup

To stop and remove all containers:

```bash
docker compose down
```

---

## Author

**Hisham Murad**  
GitHub: [@H1shamM](https://github.com/H1shamM)

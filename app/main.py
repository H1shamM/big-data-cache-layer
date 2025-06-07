from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.cache import (get_from_cache, set_in_cache, fetch_from_source,
                       REQUEST_LATENCY_HIST)
from app.cache import r as redis_client

app = FastAPI(title="Big-Data Cache Layer")
app.state.redis_client = redis_client


@app.get("/items/{key}")
def get_item(key: str):
    with REQUEST_LATENCY_HIST.time():
        cached = get_from_cache(key)
        if cached:
            return JSONResponse(
                {"key": key, "value": cached, "source": "cache"}
            )

        from_source = fetch_from_source(key)
        set_in_cache(key, from_source)

        return JSONResponse(
            {"key": key, "value": from_source, "source": "origin"}
        )


@app.get("/metrics")
def metrics():
    """
        Return Prometheus metrics as plaintext.
    """
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health():
    try:
        app.state.redis_client.get("health")
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unreachable")

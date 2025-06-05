from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import Histogram
from app.cache import get_from_cache, set_in_cache, fetch_from_source, REQUEST_LATENCY_HIST

app = FastAPI(title="Big-Data Cache Layer")

@app.get("/items/{key}")
def get_item(key: str):
    with REQUEST_LATENCY_HIST.time():
        cached = get_from_cache(key)
        if cached:
            return JSONResponse({"key": key, "value": cached, "source": "cache"})


        from_source = fetch_from_source(key)
        set_in_cache(key, from_source)

        return JSONResponse({"key": key, "value": from_source, "source": "origin"})

@app.get("/metrics")
def metrics():
    """
        Return Prometheus metrics as plaintext.
    """
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)
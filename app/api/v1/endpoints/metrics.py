from fastapi import APIRouter
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

router = APIRouter()

# Metrics Definitions
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])
DEPLOYMENT_COUNT = Counter("deployments_total", "Total deployments triggered", ["status"])

@router.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Middleware-like logic to be used in main.py or as a dependency
async def track_request_metrics(method: str, endpoint: str, status_code: int, duration: float):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

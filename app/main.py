from fastapi import FastAPI, Request
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.endpoints import metrics
import time

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
)

# Include the versioned API router
app.include_router(api_router)
app.include_router(metrics.router, tags=["Observability"])

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Track metrics for Prometheus
    from app.api.v1.endpoints.metrics import track_request_metrics
    await track_request_metrics(
        method=request.method, 
        endpoint=request.url.path, 
        status_code=response.status_code, 
        duration=duration
    )
    return response

@app.get("/healthcheck", tags=["Health"])
async def health_check():
    logger.info("Health check performed")
    return {"status": "healthy", "version": settings.VERSION}

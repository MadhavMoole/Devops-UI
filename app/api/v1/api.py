from fastapi import APIRouter
from app.api.v1.endpoints import auth, applications, deployments, pipelines, websocket

api_router = APIRouter()

# Aggregate all domain routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(deployments.router, prefix="/deployments", tags=["Deployments"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["Pipelines"])
api_router.include_router(websocket.router, tags=["Real-time"])

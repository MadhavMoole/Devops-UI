from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.application import ApplicationCreate, ApplicationRead, EnvironmentCreate, EnvironmentRead
from app.services.app_service import ApplicationService
from app.api.v1.dependencies import get_db, get_current_user, RoleChecker
from app.models.user import UserRole

router = APIRouter()

# Only Admin and DevOps can manage applications
admin_devops_only = Depends(RoleChecker([UserRole.ADMIN, UserRole.DEVOPS]))

@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application(
    app_in: ApplicationCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(admin_devops_only)
):
    service = ApplicationService(db)
    return service.create_application(app_in)

@router.get("/", response_model=list[ApplicationRead])
async def list_applications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ApplicationService(db)
    return service.list_applications()

@router.get("/{app_id}", response_model=ApplicationRead)
async def get_application(
    app_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ApplicationService(db)
    return service.get_application(app_id)

@router.post("/{app_id}/environments", response_model=EnvironmentRead, status_code=status.HTTP_201_CREATED)
async def add_environment(
    app_id: int, 
    env_in: EnvironmentCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(admin_devops_only)
):
    service = ApplicationService(db)
    return service.add_environment(app_id, env_in)

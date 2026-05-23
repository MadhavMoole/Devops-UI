from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.deployment import DeploymentCreate, DeploymentRead
from app.services.deploy_service import DeploymentService
from app.api.v1.dependencies import get_db, get_current_user, RoleChecker
from app.models.user import UserRole

router = APIRouter()

# Only Admin and DevOps can trigger deployments
admin_devops_only = Depends(RoleChecker([UserRole.ADMIN, UserRole.DEVOPS]))

@router.post("/", response_model=DeploymentRead, status_code=status.HTTP_201_CREATED)
async def trigger_deployment(
    deploy_in: DeploymentCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(admin_devops_only)
):
    service = DeploymentService(db)
    return service.trigger_deployment(deploy_in, current_user.id)

@router.get("/{deploy_id}", response_model=DeploymentRead)
async def get_deployment(
    deploy_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = DeploymentService(db)
    return service.get_deployment_status(deploy_id)

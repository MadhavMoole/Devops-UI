from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.deploy_repo import DeploymentRepository
from app.schemas.deployment import DeploymentCreate, DeploymentRead
from app.worker.tasks import execute_deployment_task

class DeploymentService:
    def __init__(self, db: Session):
        self.repo = DeploymentRepository(db)

    def trigger_deployment(self, deploy_in: DeploymentCreate, user_id: int) -> DeploymentRead:
        # Create record in DB
        deployment = self.repo.create(deploy_in, user_id)
        
        # Dispatch to Celery worker with full context
        execute_deployment_task.delay(
            deployment.id, 
            deployment.application_id, 
            deployment.environment_id, 
            deployment.commit_hash
        )
        
        return deployment

    def get_deployment_status(self, deploy_id: int) -> DeploymentRead:
        deploy = self.repo.get(deploy_id)
        if not deploy:
            raise HTTPException(status_code=404, detail="Deployment not found")
        return deploy

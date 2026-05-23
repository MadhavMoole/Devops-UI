from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.deployment import Deployment, DeploymentStatus
from app.schemas.deployment import DeploymentCreate

class DeploymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, deploy_in: DeploymentCreate, user_id: int) -> Deployment:
        db_deploy = Deployment(
            application_id=deploy_in.application_id,
            environment_id=deploy_in.environment_id,
            commit_hash=deploy_in.commit_hash,
            triggered_by=user_id,
            status=DeploymentStatus.PENDING
        )
        self.db.add(db_deploy)
        self.db.commit()
        self.db.refresh(db_deploy)
        return db_deploy

    def get(self, deploy_id: int) -> Deployment | None:
        return self.db.execute(select(Deployment).where(Deployment.id == deploy_id)).scalar_one_or_none()

    def update_status(self, deploy_id: int, status: DeploymentStatus, log: str = None, external_id: str = None) -> Deployment:
        deploy = self.get(deploy_id)
        if deploy:
            deploy.status = status
            if log: deploy.log_output = log
            if external_id: deploy.external_job_id = external_id
            self.db.commit()
            self.db.refresh(deploy)
        return deploy

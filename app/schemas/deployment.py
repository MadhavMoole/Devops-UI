from pydantic import BaseModel, Field
from app.models.deployment import DeploymentStatus

class DeploymentCreate(BaseModel):
    application_id: int
    environment_id: int
    commit_hash: str = Field(..., min_length=7, max_length=100)

class DeploymentRead(BaseModel):
    id: int
    application_id: int
    environment_id: int
    status: DeploymentStatus
    commit_hash: str
    triggered_by: int
    log_output: str | None = None
    external_job_id: str | None = None

    class Config:
        from_attributes = True

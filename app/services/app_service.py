from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.app_repo import ApplicationRepository, EnvironmentRepository
from app.schemas.application import ApplicationCreate, ApplicationRead, EnvironmentCreate, EnvironmentRead

class ApplicationService:
    def __init__(self, db: Session):
        self.app_repo = ApplicationRepository(db)
        self.env_repo = EnvironmentRepository(db)

    def create_application(self, app_in: ApplicationCreate) -> ApplicationRead:
        return self.app_repo.create(app_in)

    def get_application(self, app_id: int) -> ApplicationRead:
        app = self.app_repo.get(app_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        return app

    def list_applications(self) -> list[ApplicationRead]:
        return self.app_repo.list()

    def add_environment(self, app_id: int, env_in: EnvironmentCreate) -> EnvironmentRead:
        # Verify app exists
        self.get_application(app_id)
        return self.env_repo.create(app_id, env_in)

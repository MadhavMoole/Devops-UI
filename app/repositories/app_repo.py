from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.application import Application, Environment, EnvironmentVariable
from app.schemas.application import ApplicationCreate, EnvironmentCreate

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, app_in: ApplicationCreate) -> Application:
        db_app = Application(
            name=app_in.name,
            description=app_in.description,
            repository_url=str(app_in.repository_url)
        )
        self.db.add(db_app)
        self.db.commit()
        self.db.refresh(db_app)
        return db_app

    def get(self, app_id: int) -> Application | None:
        return self.db.execute(select(Application).where(Application.id == app_id)).scalar_one_or_none()

    def list(self) -> list[Application]:
        return self.db.execute(select(Application)).scalars().all()

class EnvironmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, app_id: int, env_in: EnvironmentCreate) -> Environment:
        db_env = Environment(
            application_id=app_id,
            name=env_in.name,
            branch=env_in.branch
        )
        self.db.add(db_env)
        self.db.flush() # Get env_id before adding variables

        for var in env_in.variables:
            db_var = EnvironmentVariable(
                environment_id=db_env.id,
                key=var.key,
                value=var.value,
                is_secret=var.is_secret
            )
            self.db.add(db_var)
        
        self.db.commit()
        self.db.refresh(db_env)
        return db_env

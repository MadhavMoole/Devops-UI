import enum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class DeploymentStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Deployment(Base, TimestampMixin):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False)
    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"), nullable=False)
    status: Mapped[DeploymentStatus] = mapped_column(Enum(DeploymentStatus), default=DeploymentStatus.PENDING, nullable=False)
    commit_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    triggered_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    log_output: Mapped[str] = mapped_column(String, nullable=True)
    external_job_id: Mapped[str] = mapped_column(String(255), nullable=True) # GitHub Action Run ID

    application: Mapped["Application"] = relationship()
    environment: Mapped["Environment"] = relationship()

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

class Application(Base, TimestampMixin):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    repository_url: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relationships
    environments: Mapped[list["Environment"]] = relationship(back_populates="application", cascade="all, delete-orphan")

class Environment(Base, TimestampMixin):
    __tablename__ = "environments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., "production", "staging"
    branch: Mapped[str] = mapped_column(String(100), nullable=False) # Branch associated with this env
    
    # Relationships
    application: Mapped["Application"] = relationship(back_populates="environments")
    variables: Mapped[list["EnvironmentVariable"]] = relationship(back_populates="environment", cascade="all, delete-orphan")

class EnvironmentVariable(Base, TimestampMixin):
    __tablename__ = "environment_variables"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    environment_id: Mapped[int] = mapped_column(ForeignKey("environments.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(1000), nullable=False) # In a real prod app, this would be encrypted
    is_secret: Mapped[bool] = mapped_column(default=False)

    environment: Mapped["Environment"] = relationship(back_populates="variables")

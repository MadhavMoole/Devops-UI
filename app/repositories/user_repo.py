from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User, UserRole
from app.schemas.auth import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            role=user_in.role,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

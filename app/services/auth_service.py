from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserCreate, UserRead
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> UserRead:
        if self.repo.get_by_username(user_in.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pw = get_password_hash(user_in.password)
        user = self.repo.create(user_in, hashed_pw)
        return user

    def authenticate_user(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(subject=user.username)
        return {"access_token": access_token, "token_type": "bearer"}

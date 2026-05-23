from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenRequest="jwt")

# This is a mock DB session provider for now until we implement the DB engine in Step 2
def get_db():
    # In Step 2, this will yield a real SQLAlchemy session
    raise NotImplementedError("Database session not yet implemented. See Step 2.")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    user = UserRepository(db).get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to perform this action"
            )
        return user

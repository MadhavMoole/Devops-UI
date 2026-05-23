from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.DEVELOPER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token:
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: UserRole | None = None

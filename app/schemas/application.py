from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class EnvVarBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str
    is_secret: bool = False

class EnvVarCreate(EnvVarBase):
    pass

class EnvVarRead(EnvVarBase):
    id: int
    class Config:
        from_attributes = True

class EnvironmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    branch: str = Field(..., min_length=1, max_length=100)

class EnvironmentCreate(EnvironmentBase):
    variables: List[EnvVarCreate] = []

class EnvironmentRead(EnvironmentBase):
    id: int
    application_id: int
    variables: List[EnvVarRead] = []
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    repository_url: HttpUrl

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationRead(ApplicationBase):
    id: int
    environments: List[EnvironmentRead] = []
    class Config:
        from_attributes = True

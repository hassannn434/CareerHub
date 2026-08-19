from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from uuid import UUID

class Role(str, Enum):
    student = "student"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Role = Role.student

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: Role

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None

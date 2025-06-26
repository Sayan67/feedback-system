from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID
from datetime import datetime

class RoleEnum(str, Enum):
    manager = "manager"
    employee = "employee"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: RoleEnum
    created_at: datetime

    class Config:
        orm_mode = True

from typing import Literal, Optional
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

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: UUID

    class Config:
        orm_mode = True

class FeedbackCreate(BaseModel):
    employee_id: UUID
    strengths: str
    areas_to_improve: str
    sentiment: Literal["positive", "neutral", "negative"]
    tags: list[str] = []


class FeedbackResponse(BaseModel):
    id: UUID
    strengths: str
    areas_to_improve: str
    sentiment: str
    tags: list[TagResponse]
    acknowledged: Optional[bool] = False
    employee_reply: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SentimentBreakdown(BaseModel):
    positive: int = 0
    neutral: int = 0
    negative: int = 0

class EmployeeFeedbackSummary(BaseModel):
    employee_id: UUID
    employee_name: str
    feedback_count: int
    sentiments: SentimentBreakdown

class FeedbackAcknowledgeUpdate(BaseModel):
    reply: Optional[str] = None


class FeedbackRequestCreate(BaseModel):
    manager_id: UUID
    message: Optional[str] = None

class FeedbackRequestResponse(BaseModel):
    id: UUID
    manager_id: UUID
    employee_id: UUID
    message: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

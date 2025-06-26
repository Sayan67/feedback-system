from sqlalchemy import Column, String, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from .database import Base

from sqlalchemy import CheckConstraint

class RoleEnum(str, enum.Enum):
    manager = "manager"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    __table_args__ = (CheckConstraint("role IN ('manager', 'employee')", name="check_role_valid"),)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

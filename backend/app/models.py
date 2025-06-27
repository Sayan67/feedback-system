from sqlalchemy import Column, ForeignKey, String, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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

class Tag(Base):
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    feedbacks = relationship(
        "Feedback",
        secondary="feedback_tags",
        back_populates="tags"
    )

class FeedbackTag(Base):
    __tablename__ = "feedback_tags"
    feedback_id = Column(UUID(as_uuid=True), ForeignKey("feedbacks.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # manager_id, employee_id, etc...

    tags = relationship(
        "Tag",
        secondary="feedback_tags",
        back_populates="feedbacks"
    )

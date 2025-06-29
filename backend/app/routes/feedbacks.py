from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID, uuid4

from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from fastapi import Depends

from app.auth import get_current_user



router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"],)

# Create feedback
@router.post("/", response_model=schemas.FeedbackResponse)
async def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can create feedback")

    new_feedback = models.Feedback(
        id=uuid4(),
        manager_id=current_user.id,
        employee_id=feedback.employee_id,
        strengths=feedback.strengths,
        areas_to_improve=feedback.areas_to_improve,
        sentiment=feedback.sentiment,
    )

    tag_objs = []
    for tag_name in feedback.tags:
        stmt = select(models.Tag).where(models.Tag.name == tag_name)
        result = await db.execute(stmt)
        tag = result.scalar_one_or_none()
        if not tag:
            tag = models.Tag(id=uuid4(), name=tag_name)
            db.add(tag)
            await db.flush()
        tag_objs.append(tag)

    new_feedback.tags = tag_objs

    db.add(new_feedback)
    await db.commit()
    stmt = select(models.FeedbackRequest).where(
    models.FeedbackRequest.manager_id == current_user.id,
    models.FeedbackRequest.employee_id == feedback.employee_id,
    models.FeedbackRequest.status == "pending"
)
    result = await db.execute(stmt)
    request = result.scalar_one_or_none()
    if request:
        setattr(request, 'status', "fulfilled")
        await db.commit()
    stmt = (
    select(models.Feedback)
        .where(models.Feedback.id == new_feedback.id)
        .options(selectinload(models.Feedback.tags))
    )
    result = await db.execute(stmt)
    new_feedback = result.scalar_one()
    return new_feedback


# Get feedbacks for employee
@router.get("/me", response_model=list[schemas.FeedbackResponse])
async def my_feedbacks(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if str(current_user.role) != "employee":
        raise HTTPException(status_code=403, detail="Only employees can view this")

    stmt = (
        select(models.Feedback)
        .where(models.Feedback.employee_id == current_user.id)
        .options(selectinload(models.Feedback.tags))
        .order_by(models.Feedback.created_at.desc())
    )
    result = await db.execute(stmt)
    feedbacks = result.scalars().all()

    return feedbacks

# Acknowledge feedback
@router.patch("/{feedback_id}/acknowledge", response_model=schemas.FeedbackResponse)
async def acknowledge_feedback(
    feedback_id: UUID,
    data: schemas.FeedbackAcknowledgeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if str(current_user.role) != "employee":
        raise HTTPException(status_code=403, detail="Only employees can acknowledge feedback")

    stmt = select(models.Feedback).where(models.Feedback.id == feedback_id)
    result = await db.execute(stmt)
    feedback = result.scalar_one_or_none()

    if not feedback or str(feedback.employee_id) != str(current_user.id):
        raise HTTPException(status_code=404, detail="Feedback not found or unauthorized")

    setattr(feedback, 'acknowledged', True)
    if data.reply:
        setattr(feedback, 'employee_reply', data.reply)

    await db.commit()
    stmt = (
    select(models.Feedback)
        .where(models.Feedback.id == feedback_id)
        .options(selectinload(models.Feedback.tags))
    )
    result = await db.execute(stmt)
    feedback = result.scalar_one()
    return feedback

@router.get("/employee/{employee_id}", response_model=list[schemas.FeedbackResponse])
async def get_feedbacks_for_employee(
    employee_id: UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view this")

    stmt = (
        select(models.Feedback)
        .where(
            models.Feedback.manager_id == current_user.id,
            models.Feedback.employee_id == employee_id,
        )
        .options(selectinload(models.Feedback.tags))
        .order_by(models.Feedback.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()





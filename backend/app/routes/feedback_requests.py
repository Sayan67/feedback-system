from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from sqlalchemy.orm import selectinload
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from app.utils import send_email

router = APIRouter(prefix="/feedback-requests", tags=["Employee"])

@router.post("/", response_model=schemas.FeedbackRequestResponse)
async def request_feedback(
    request: schemas.FeedbackRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if str(current_user.role) != "employee":
        raise HTTPException(status_code=403, detail="Only employees can request feedback")

    feedback_request = models.FeedbackRequest(
        id=uuid4(),
        employee_id=current_user.id,
        manager_id=request.manager_id,
        message=request.message
    )

    db.add(feedback_request)
    await db.commit()

    # Fetch manager's email
    stmt = select(models.User).where(models.User.id == request.manager_id)
    result = await db.execute(stmt)
    manager = result.scalar_one_or_none()

    if manager:
        subject = f"📩 Feedback Request from {current_user.name}"
        body = (
            f"Hi {manager.name},\n\n"
            f"You have a new feedback request from {current_user.name}.\n"
            f"Message: {request.message or 'No message provided.'}\n\n"
            f"Please log in to the feedback system to respond.\n\nThanks!"
        )
        send_email(str(manager.email), subject, body)

    # Return created feedback request
    stmt = select(models.FeedbackRequest).where(models.FeedbackRequest.id == feedback_request.id)
    result = await db.execute(stmt)
    feedback_request = result.scalar_one()
    return feedback_request

@router.get("/my-manager", response_model=schemas.UserOut)
async def get_my_manager(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if str(current_user.role) != "employee":
        raise HTTPException(status_code=403, detail="Only employees can view their manager")

    stmt = (
        select(models.User)
        .join(models.Team, models.User.id == models.Team.manager_id)
        .where(models.Team.employee_id == current_user.id)
    )
    result = await db.execute(stmt)
    manager = result.scalar_one_or_none()

    if not manager:
        raise HTTPException(status_code=404, detail="No manager assigned")
    
    return manager

@router.get("/notifications", response_model=list[schemas.FeedbackRequestResponse])
async def get_feedback_requests_for_manager(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view feedback requests")

    stmt = (
        select(models.FeedbackRequest)
        .where(models.FeedbackRequest.manager_id == current_user.id)
        .options(selectinload(models.FeedbackRequest.employee))
        .order_by(models.FeedbackRequest.created_at.desc())
    )
    result = await db.execute(stmt)
    requests = result.scalars().all()
    return requests
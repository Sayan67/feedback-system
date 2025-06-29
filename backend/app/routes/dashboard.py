from fastapi import APIRouter, Depends, HTTPException 
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from app import models

router = APIRouter()

@router.get("/dashboard", tags=["Manager"])
async def manager_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can access the dashboard")

    stmt = (
        select(models.Feedback)
        .where(models.Feedback.manager_id == current_user.id)
        .options(selectinload(models.Feedback.employee))
    )
    result = await db.execute(stmt)
    feedbacks = result.scalars().all()

    # Sentiment breakdown
    sentiment_counts = {
        "positive": 0,
        "neutral": 0,
        "negative": 0,
    }
    for fb in feedbacks:
        sentiment_counts[str(fb.sentiment)] += 1

    # Group by employee
    grouped = {}
    for fb in feedbacks:
        emp = fb.employee
        if emp.id not in grouped:
            grouped[emp.id] = {
                "employee_id": str(emp.id),
                "employee_name": emp.name,
                "feedback_count": 0,
                "feedbacks": [],
            }
        grouped[emp.id]["feedback_count"] += 1
        grouped[emp.id]["feedbacks"].append({
            "id": str(fb.id),
            "sentiment": fb.sentiment,
            "created_at": fb.created_at,
        })

    return {
        "sentiment_summary": sentiment_counts,
        "team_feedback": list(grouped.values()),
    }


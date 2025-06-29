from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import not_, exists
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(tags=["Manager"])

@router.get("/unassigned-employees", response_model=list[schemas.UserOut])
async def get_unassigned_employees(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can view unassigned employees")

    # Query for employees who are not assigned in the teams table
    subquery = select(models.Team.employee_id)
    stmt = (
        select(models.User)
        .where(
            models.User.role == "employee",
            ~models.User.id.in_(subquery)
        )
    )
    result = await db.execute(stmt)
    unassigned = result.scalars().all()
    return unassigned

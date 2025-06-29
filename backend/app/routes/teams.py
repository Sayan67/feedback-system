from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from uuid import UUID

from app.database import get_db
from app import models
from app.auth import get_current_user

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/assign")
async def assign_employee_to_manager(
    employee_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if str(current_user.role) != "manager":
        raise HTTPException(status_code=403, detail="Only managers can assign employees")

    # Check if employee exists
    stmt = select(models.User).where(models.User.id == employee_id, models.User.role == "employee")
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if already assigned
    stmt = select(models.Team).where(
        models.Team.manager_id == current_user.id,
        models.Team.employee_id == employee_id
    )
    existing = await db.execute(stmt)
    if existing.scalar():
        raise HTTPException(status_code=400, detail="Employee is already in your team")

    # Insert into team
    new_team_entry = models.Team(manager_id=current_user.id, employee_id=employee_id)
    db.add(new_team_entry)
    await db.commit()

    return {"detail": f"Employee {employee.name} assigned to your team."}

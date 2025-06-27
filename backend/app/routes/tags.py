from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=schemas.TagResponse)
async def create_tag(tag: schemas.TagCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(models.Tag).where(models.Tag.name == tag.name)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = models.Tag(id=uuid4(), name=tag.name)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag

@router.get("/", response_model=list[schemas.TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Tag))
    return result.scalars().all()

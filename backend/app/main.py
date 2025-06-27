from contextlib import asynccontextmanager
from sqlite3 import IntegrityError
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, AsyncSessionLocal, get_db
from app import models, schemas
from app.utils import hash_password
from app.routes import tags

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Connected to PostgreSQL")
    except Exception as e:
        print("❌ DB Connection Error:", e)
    yield

app = FastAPI(lifespan=lifespan)



@app.post("/users/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pw,
        role=user.role,
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/")
async def root():
    return {"message": "Feedback System API is live"}

app.include_router(tags.router)
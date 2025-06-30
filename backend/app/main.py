from contextlib import asynccontextmanager
from sqlite3 import IntegrityError
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, AsyncSessionLocal, get_db
from app import models, schemas
from app.utils import hash_password
from app.routes import tags
from app.routes import feedbacks
from app.routes import dashboard
from app.routes import auth
from app.routes import feedback_requests
from app.routes import teams
from app.routes import unassigned_employees
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Connected to PostgreSQL")
    except Exception as e:
        print("DB Connection Error:", e)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Feedback System API is live"}

app.include_router(tags.router)
app.include_router(feedbacks.router)
app.include_router(dashboard.router)
app.include_router(feedback_requests.router)
app.include_router(teams.router)
app.include_router(unassigned_employees.router)
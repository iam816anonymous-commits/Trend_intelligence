from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.storage.database import get_async_db
from backend.storage.models import Signal, Topic, Opportunity, Knowledge, LearningLog
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Annotated
import datetime

router = APIRouter(prefix="/api/v1")

class SignalOut(BaseModel):
    id: int
    title: str
    source: str
    region: str
    timestamp: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class TopicOut(BaseModel):
    id: int
    name: str
    trend_score: float
    status: str
    confidence: float
    model_config = ConfigDict(from_attributes=True)

@router.get("/signals", response_model=List[SignalOut])
async def read_signals(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    region: Optional[str] = None
):
    stmt = select(Signal)
    if region:
        stmt = stmt.where(Signal.region == region)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/trends", response_model=List[TopicOut])
async def read_trends(db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = select(Topic).order_by(Topic.trend_score.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/knowledge")
async def read_knowledge(db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = select(Knowledge)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/learning-logs")
async def read_logs(db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = select(LearningLog).order_by(LearningLog.timestamp.desc()).limit(20)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/health")
async def health_check():
    return {"status": "operational", "version": "v1.0.0-b2b"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.storage.models import Signal, Topic, Opportunity, SessionLocal
from backend.api.config import settings
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SignalOut(BaseModel):
    id: int
    title: str
    source: str
    region: str
    timestamp: datetime.datetime
    class Config:
        from_attributes = True

class TopicOut(BaseModel):
    id: int
    name: str
    trend_score: float
    status: str
    confidence: float
    class Config:
        from_attributes = True

@router.get("/signals", response_model=List[SignalOut])
def read_signals(
    skip: int = 0,
    limit: int = 100,
    region: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Signal)
    if region:
        query = query.filter(Signal.region == region)
    if type:
        query = query.filter(Signal.type == type)
    return query.offset(skip).limit(limit).all()

@router.get("/trends", response_model=List[TopicOut])
def read_trends(db: Session = Depends(get_db)):
    return db.query(Topic).order_by(Topic.trend_score.desc()).all()

@router.get("/opportunities")
def read_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).order_by(Opportunity.evidence_score.desc()).all()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

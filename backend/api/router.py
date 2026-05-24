from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.storage.models import Article, Source, SessionLocal
from backend.collectors.rss.collector import RSSCollector
from backend.embeddings.vector_store import VectorStore
from backend.trends.detector import TrendDetector
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ArticleOut(BaseModel):
    id: int
    title: str
    source_name: str
    url: str
    category: str

    class Config:
        from_attributes = True

@router.get("/articles", response_model=List[ArticleOut])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = db.query(Article).offset(skip).limit(limit).all()
    return articles

@router.get("/sources")
def read_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()

@router.get("/semantic-search")
def semantic_search(q: str, limit: int = 5):
    vs = VectorStore()
    results = vs.search(q, limit=limit)
    return results

@router.get("/trends")
def get_trends(country: Optional[str] = "India", db: Session = Depends(get_db)):
    detector = TrendDetector()
    # Filter by country in the detector if needed
    return detector.detect_trends(db)

@router.post("/collect")
def collect_articles(db: Session = Depends(get_db)):
    sources = db.query(Source).filter(Source.is_active == 1).all()
    rss_collector = RSSCollector()

    for source in sources:
        if source.type == "rss":
            rss_collector.collect(db, source)

    return {"message": "Collection triggered"}

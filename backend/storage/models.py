from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float, ForeignKey, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine
import datetime
from backend.api.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True, nullable=False)
    body = Column(Text)
    source = Column(String(100), index=True) # reddit, blinkit, news, etc.
    url = Column(String(1000), unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    category = Column(String(100), index=True)
    region = Column(String(100), default="India", index=True)
    type = Column(String(50), index=True) # consumer, business, geo, policy
    metadata_json = Column(JSON)
    score = Column(Float, default=0.0)

    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    topic = relationship("Topic", back_populates="signals")

    __table_args__ = (
        Index('idx_signal_timestamp_type', 'timestamp', 'type'),
    )

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(Text)
    trend_score = Column(Float, default=0.0)
    velocity = Column(Float, default=0.0)
    growth = Column(Float, default=0.0)
    status = Column(String(50)) # Early, Growing, Hot, Peak, Declining
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    confidence = Column(Float, default=0.0)

    signals = relationship("Signal", back_populates="topic")

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    market_niche = Column(String(100))
    type = Column(String(50)) # D2C, SaaS, Service
    evidence_score = Column(Float)
    launch_cost_est = Column(Float)
    signals_count = Column(Integer)
    potential_roi = Column(String(50))

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    url = Column(String(500), unique=True, index=True)
    type = Column(String(50))
    category = Column(String(100))
    country = Column(String(100), default="India")
    is_active = Column(Integer, default=1)

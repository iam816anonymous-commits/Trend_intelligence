from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float, ForeignKey, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
from backend.api.config import settings
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True, nullable=False)
    body = Column(Text)
    source = Column(String(100), index=True)
    url = Column(String(1000), unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    category = Column(String(100), index=True)
    region = Column(String(100), default="India", index=True)
    type = Column(String(50), index=True) # consumer, business, geo, policy
    sentiment = Column(Float, default=0.0)
    impact_score = Column(Float, default=0.0)
    metadata_json = Column(JSON)

    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    topic = relationship("Topic", back_populates="signals")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(Text)
    trend_score = Column(Float, default=0.0)
    velocity = Column(Float, default=0.0)
    growth = Column(Float, default=0.0)
    status = Column(String(50))
    confidence = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    signals = relationship("Signal", back_populates="topic")
    history = relationship("TopicHistory", back_populates="topic")

class TopicHistory(Base):
    __tablename__ = "topic_history"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    topic = relationship("Topic", back_populates="history")

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    market_niche = Column(String(100))
    type = Column(String(50))
    evidence_score = Column(Float)
    launch_cost_est = Column(Float)
    signals_count = Column(Integer)
    potential_roi = Column(String(50))
    execution_roadmap = Column(JSON) # Steps to execute

class Knowledge(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    concept = Column(String(200), unique=True, index=True)
    definition = Column(Text)
    category = Column(String(100))
    first_detected = Column(DateTime, default=datetime.datetime.utcnow)
    strength = Column(Float, default=0.0)

class LearningLog(Base):
    __tablename__ = "learning_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(500))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    impact_area = Column(String(100))

class AgentActivity(Base):
    __tablename__ = "agent_activities"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(100))
    status = Column(String(50)) # thinking, executing, success, error
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(JSON)

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    url = Column(String(500), unique=True, index=True)
    type = Column(String(50))
    category = Column(String(100))
    country = Column(String(100), default="India")
    is_active = Column(Integer, default=1)

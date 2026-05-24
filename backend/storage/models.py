from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import datetime
from backend.api.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    source_name = Column(String)
    url = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String)
    country = Column(String, default="India")
    language = Column(String, default="English")
    raw_data = Column(JSON)
    hash = Column(String, index=True)

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    source = Column(String)  # reddit, blinkit, news, etc.
    url = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String)
    region = Column(String, default="India")
    type = Column(String)  # consumer, business, geo, policy
    metadata_json = Column(JSON)
    score = Column(Float, default=0.0)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    trend_score = Column(Float, default=0.0)
    velocity = Column(Float, default=0.0)
    growth = Column(Float, default=0.0)
    status = Column(String)  # Early, Growing, Hot, Peak, Declining
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    market_niche = Column(String)
    evidence_score = Column(Float)
    launch_cost_est = Column(Float)
    signals_count = Column(Integer)

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    type = Column(String)
    category = Column(String)
    country = Column(String, default="India")
    language = Column(String, default="English")
    is_active = Column(Integer, default=1)

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from backend.api.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    type = Column(String)  # rss, news, youtube
    category = Column(String)
    country = Column(String, default="India")
    language = Column(String, default="English")
    is_active = Column(Integer, default=1)

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

from fastapi import FastAPI
import os
import redis
import psycopg2
from qdrant_client import QdrantClient
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_DB: str = "trend_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
app = FastAPI(title="Trend Intelligence AI")

@app.get("/health")
def health_check():
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "redis": "unknown",
        "qdrant": "unknown"
    }

    # Check Postgres
    try:
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            connect_timeout=1
        )
        conn.close()
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, socket_timeout=1)
        r.ping()
        health_status["redis"] = "connected"
    except Exception as e:
        health_status["redis"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Qdrant
    try:
        qc = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, timeout=1)
        qc.get_collections()
        health_status["qdrant"] = "connected"
    except Exception as e:
        health_status["qdrant"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    return health_status

@app.get("/")
def read_root():
    return {"message": "Welcome to Trend Intelligence AI India"}

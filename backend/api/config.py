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

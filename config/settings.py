import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    # -----------------------------
    # APP CONFIG
    # -----------------------------
    APP_NAME: str = os.getenv("APP_NAME", "rag_backend")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))

    # -----------------------------
    # DATABASE
    # -----------------------------
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "rag_app")

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # -----------------------------
    # REDIS
    # -----------------------------
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"
    )

    # Vector index
    VECTOR_DIM: int = int(os.getenv("VECTOR_DIM", 768))
    REDIS_VECTOR_INDEX: str = os.getenv("REDIS_VECTOR_INDEX", "vec_index")

    # -----------------------------
    # JWT / AUTH
    # -----------------------------
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # -----------------------------
    # SECURITY
    # -----------------------------
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))

    # -----------------------------
    # RAG / AI
    # -----------------------------
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-r1:1.5b")
    VECTOR_DB: str = os.getenv("VECTOR_DB", "redis")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 50))

    # -----------------------------
    # MONITORING
    # -----------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PROMETHEUS_ENABLED: bool = os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true"

    # -----------------------------
    # EMAIL (optional)
    # -----------------------------
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")


settings = Settings()

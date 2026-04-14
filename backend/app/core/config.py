"""
IU NWEO AI — Core Configuration
Maintainer: Architect

Pydantic BaseSettings loads from .env automatically.
Docker Compose overrides these via environment variables at runtime.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Central configuration. Every service connection string lives here.
    Field priority: environment variable > .env file > default.
    """

    # --- App ---
    APP_NAME: str = "IU NWEO AI"
    APP_DEBUG: bool = Field(default=False, description="Enable debug mode")
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # --- LLM (Gemini) ---
    # Defaults to empty — app boots but LLM calls will fail until set
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")

    # --- PostgreSQL (LangGraph Checkpointer) ---
    # Format: postgresql://user:password@host:port/dbname
    # psycopg v3 driver — do NOT use psycopg2:// prefix
    DATABASE_URL: str = "postgresql://iu_user:iu_password@localhost:5432/iu_langgraph"

    # --- Neo4j (GraphRAG) ---
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "iu_neo4j_pass"

    # --- ChromaDB (Vector Store) ---
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings singleton.
    Call this instead of Settings() directly to avoid re-parsing .env on every request.
    """
    return Settings()


# Module-level convenience alias (used by existing code: `from app.core.config import settings`)
settings = get_settings()

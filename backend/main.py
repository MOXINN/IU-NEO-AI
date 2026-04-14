"""
IU NWEO AI — FastAPI Application Factory
Maintainer: Architect

The single entry point. Lifespan manages all service connections.
Ops exposes this on port 8080 via Docker or `uvicorn main:app --reload`.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db_pool, close_db_pool
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("iu-nweo")


# ============================================================================
# Lifespan: startup/shutdown lifecycle
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages connections to all external services.
    Phase 1: PostgreSQL only.
    Phase 2+: ChromaDB client, Neo4j driver will be added here.
    """
    logger.info("=" * 60)
    logger.info("IU NWEO AI — Starting up...")
    logger.info("=" * 60)

    # --- Startup ---
    try:
        # PostgreSQL (LangGraph Checkpointer)
        db_pool = await init_db_pool()
        app.state.db_pool = db_pool
        logger.info("✓ PostgreSQL connected")
    except Exception as e:
        logger.warning(f"✗ PostgreSQL unavailable: {e}")
        logger.warning("  Continuing without persistence (in-memory mode)")
        app.state.db_pool = None

    # TODO Phase 3: ChromaDB client init
    # TODO Phase 3: Neo4j driver init

    logger.info("=" * 60)
    logger.info("IU NWEO AI — Ready to serve")
    logger.info("=" * 60)

    yield  # App runs here

    # --- Shutdown ---
    logger.info("IU NWEO AI — Shutting down...")
    await close_db_pool()
    logger.info("IU NWEO AI — Goodbye.")


# ============================================================================
# App factory
# ============================================================================
app = FastAPI(
    title=settings.APP_NAME,
    description="Integral University AI Assistant — Agentic RAG System",
    version="0.2.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.APP_DEBUG else None,
    redoc_url="/redoc" if settings.APP_DEBUG else None,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Routes
# ============================================================================
from app.api.routes import chat, health  # noqa: E402

app.include_router(
    chat.router,
    prefix="/api/v1/chat",
    tags=["Chat"],
)
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["System"],
)


# --- Root redirect to docs ---
@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": settings.APP_NAME,
        "version": "0.2.0",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "status": "operational",
    }

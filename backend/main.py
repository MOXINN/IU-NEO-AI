"""
IU NWEO AI — FastAPI Application Factory
Maintainer: Architect

The single entry point. Clean app factory that delegates to:
  - app.core.lifespan    → startup/shutdown lifecycle
  - app.core.middleware   → error handlers & request logging
  - app.api.routes.*      → route registration
"""

# ---------------------------------------------------------------------------
# P0 FIX: Windows Event Loop Policy
# psycopg v3 (async) requires SelectorEventLoop on Windows.
# Uvicorn defaults to ProactorEventLoop which is incompatible with libpq.
# This MUST run before any async import touches the loop.
# ---------------------------------------------------------------------------
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("iu-nweo")


# ============================================================================
# App Factory
# ============================================================================
app = FastAPI(
    title=settings.APP_NAME,
    description="Integral University AI Assistant — Agentic RAG System",
    version="0.3.0",
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

# --- Middleware (error handlers, request logging) ---
register_middleware(app)


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


# --- Root info ---
@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": settings.APP_NAME,
        "version": "0.3.0",
        "docs": "/docs" if settings.APP_DEBUG else "disabled",
        "status": "operational",
    }

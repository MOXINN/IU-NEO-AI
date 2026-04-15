"""
IU NWEO AI — Application Lifespan
Maintainer: Architect

Manages all external service connections during startup/shutdown.
Each service init is independent — failures are logged and the app
continues in degraded mode rather than crashing.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import init_db_pool, close_db_pool
import logging

logger = logging.getLogger("iu-nweo.lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages connections to all external services.
    Each service is initialized independently with graceful fallback.
    """
    logger.info("=" * 60)
    logger.info("IU NWEO AI — Starting up...")
    logger.info("=" * 60)

    # --- 1. PostgreSQL (LangGraph Checkpointer) ---
    try:
        db_pool = await init_db_pool()
        app.state.db_pool = db_pool
        logger.info("✓ PostgreSQL connected")
    except Exception as e:
        logger.warning(f"✗ PostgreSQL unavailable: {e}")
        logger.warning("  Continuing without persistence (in-memory mode)")
        app.state.db_pool = None

    # --- 2. ChromaDB (Vector Store) ---
    try:
        from app.ai.rag.vector_store import get_chroma_client
        client = get_chroma_client()
        heartbeat = client.heartbeat()
        app.state.chroma_available = True
        logger.info(f"✓ ChromaDB connected (heartbeat: {heartbeat})")
    except Exception as e:
        logger.warning(f"✗ ChromaDB unavailable: {e}")
        logger.warning("  Vector search will return empty results")
        app.state.chroma_available = False

    # --- 3. Neo4j (Knowledge Graph) ---
    try:
        from app.ai.rag.graph_store import get_graph_store
        graph = get_graph_store()
        if graph:
            app.state.neo4j_available = True
            logger.info("✓ Neo4j connected")
        else:
            app.state.neo4j_available = False
            logger.warning("✗ Neo4j returned None")
    except Exception as e:
        logger.warning(f"✗ Neo4j unavailable: {e}")
        logger.warning("  Graph search will return empty results")
        app.state.neo4j_available = False

    # --- 4. Semantic Router (FastEmbed) ---
    try:
        from app.ai.routing.semantic_router import get_route_layer
        get_route_layer()  # Pre-warm the encoder + routes
        app.state.semantic_router_available = True
        logger.info("✓ Semantic Router initialized")
    except Exception as e:
        logger.warning(f"✗ Semantic Router init failed: {e}")
        logger.warning("  Fast-path routing disabled, all queries go through LangGraph")
        app.state.semantic_router_available = False

    logger.info("=" * 60)
    logger.info("IU NWEO AI — Ready to serve")
    logger.info("=" * 60)

    yield  # App runs here

    # --- Shutdown ---
    logger.info("IU NWEO AI — Shutting down...")
    await close_db_pool()
    logger.info("IU NWEO AI — Goodbye.")

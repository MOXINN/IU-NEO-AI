"""
IU NWEO AI — Database Connection Management
Maintainer: Architect

Provides async PostgreSQL connection pool for the LangGraph checkpointer.
Uses psycopg v3 (async) with connection pooling.
"""

from psycopg_pool import AsyncConnectionPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Module-level pool reference (initialized during app lifespan)
_pool: AsyncConnectionPool | None = None


async def init_db_pool() -> AsyncConnectionPool:
    """
    Initialize the async connection pool.
    Called once during FastAPI lifespan startup.

    Key: reconnect_timeout limits internal retry duration so that
    pool.open() will raise PoolTimeout instead of retrying forever
    when PostgreSQL is unreachable.
    """
    global _pool
    logger.info("Initializing PostgreSQL connection pool...")
    _pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        min_size=2,
        max_size=10,
        open=False,           # We open explicitly below
        timeout=5.0,          # Max seconds to acquire a connection
        reconnect_timeout=5,  # Stop internal retries after 5 seconds
    )
    await _pool.open(wait=True, timeout=10.0)  # Hard cap — raises after 10s
    # Verify connectivity
    async with _pool.connection() as conn:
        await conn.execute("SELECT 1")
    logger.info("PostgreSQL connection pool ready.")
    return _pool


async def close_db_pool() -> None:
    """Gracefully close the connection pool during shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("PostgreSQL connection pool closed.")


def get_db_pool() -> AsyncConnectionPool:
    """
    Get the active connection pool.
    Raises if called before lifespan init.
    """
    if _pool is None:
        raise RuntimeError(
            "Database pool not initialized. "
            "Ensure the FastAPI lifespan has started."
        )
    return _pool

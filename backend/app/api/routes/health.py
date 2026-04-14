"""
IU NWEO AI — Health Check Endpoint
Maintainer: Architect / Ops

Reports connectivity status for all backing services.
Ops uses this for Docker health checks and monitoring.
"""

from fastapi import APIRouter, Request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """
    Returns the health status of all service dependencies.
    Each service reports 'ok', 'degraded', or 'unavailable'.
    """
    status = {
        "status": "operational",
        "services": {}
    }

    # --- PostgreSQL ---
    try:
        pool = request.app.state.db_pool
        if pool:
            async with pool.connection() as conn:
                await conn.execute("SELECT 1")
            status["services"]["postgres"] = "ok"
        else:
            status["services"]["postgres"] = "unavailable"
    except Exception as e:
        logger.warning(f"Health check — Postgres failed: {e}")
        status["services"]["postgres"] = "unavailable"

    # TODO Phase 3: ChromaDB heartbeat check
    status["services"]["chroma"] = "not_configured"

    # TODO Phase 3: Neo4j connectivity check
    status["services"]["neo4j"] = "not_configured"

    # Set overall status
    service_values = list(status["services"].values())
    if all(v == "ok" for v in service_values):
        status["status"] = "healthy"
    elif any(v == "unavailable" for v in service_values):
        status["status"] = "degraded"

    return status

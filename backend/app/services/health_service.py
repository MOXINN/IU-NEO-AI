"""
IU NWEO AI — Health Service
Maintainer: Architect

Business logic for health checking all external service dependencies.
"""

import logging
from fastapi import Request
from app.models.health import HealthResponse, OverallStatus, ServiceStatus

logger = logging.getLogger("iu-nweo.services.health")


async def check_health(request: Request) -> HealthResponse:
    """
    Checks all backing services and returns a structured health report.
    """
    services: dict[str, ServiceStatus] = {}

    # --- PostgreSQL ---
    try:
        pool = getattr(request.app.state, "db_pool", None)
        if pool:
            async with pool.connection() as conn:
                await conn.execute("SELECT 1")
            services["postgres"] = ServiceStatus.OK
        else:
            services["postgres"] = ServiceStatus.UNAVAILABLE
    except Exception as e:
        logger.warning(f"Health check — Postgres failed: {e}")
        services["postgres"] = ServiceStatus.UNAVAILABLE

    # --- ChromaDB ---
    try:
        chroma_ok = getattr(request.app.state, "chroma_available", False)
        if chroma_ok:
            from app.ai.rag.vector_store import get_chroma_client
            client = get_chroma_client()
            client.heartbeat()
            services["chroma"] = ServiceStatus.OK
        else:
            services["chroma"] = ServiceStatus.UNAVAILABLE
    except Exception as e:
        logger.warning(f"Health check — ChromaDB failed: {e}")
        services["chroma"] = ServiceStatus.UNAVAILABLE

    # --- Neo4j ---
    try:
        neo4j_ok = getattr(request.app.state, "neo4j_available", False)
        if neo4j_ok:
            services["neo4j"] = ServiceStatus.OK
        else:
            services["neo4j"] = ServiceStatus.UNAVAILABLE
    except Exception as e:
        logger.warning(f"Health check — Neo4j failed: {e}")
        services["neo4j"] = ServiceStatus.UNAVAILABLE

    # --- Semantic Router ---
    sr_ok = getattr(request.app.state, "semantic_router_available", False)
    services["semantic_router"] = ServiceStatus.OK if sr_ok else ServiceStatus.UNAVAILABLE

    # --- Determine Overall Status ---
    values = list(services.values())
    if all(v == ServiceStatus.OK for v in values):
        overall = OverallStatus.HEALTHY
    elif services.get("postgres") == ServiceStatus.OK:
        # Core DB is up, but some optional services are down
        overall = OverallStatus.OPERATIONAL
    else:
        overall = OverallStatus.DEGRADED

    return HealthResponse(status=overall, services=services)

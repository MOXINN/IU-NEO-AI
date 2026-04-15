"""
IU NWEO AI — Health Check Route
Maintainer: Architect / Ops

Thin controller — delegates to health_service for actual checks.
Reports connectivity status for all backing services.
"""

import logging
from fastapi import APIRouter, Request

from app.models.health import HealthResponse
from app.services.health_service import check_health

logger = logging.getLogger("iu-nweo.routes.health")
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    """
    Returns the health status of all service dependencies.
    Each service reports 'ok', 'degraded', or 'unavailable'.
    """
    return await check_health(request)

"""
IU NWEO AI — Health DTOs
Maintainer: Architect

Pydantic models for the health check endpoint.
"""

from pydantic import BaseModel
from enum import Enum
from typing import Dict


class ServiceStatus(str, Enum):
    """Possible states for a backing service."""
    OK = "ok"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    NOT_CONFIGURED = "not_configured"


class OverallStatus(str, Enum):
    """Overall system health."""
    HEALTHY = "healthy"
    OPERATIONAL = "operational"
    DEGRADED = "degraded"


class HealthResponse(BaseModel):
    """Response from the /health endpoint."""
    status: OverallStatus
    services: Dict[str, ServiceStatus]

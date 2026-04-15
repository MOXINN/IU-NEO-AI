"""
IU NWEO AI — FastAPI Dependencies
Maintainer: Architect

Dependency injection functions for use with FastAPI's Depends().
"""

from fastapi import Request
from psycopg_pool import AsyncConnectionPool


def get_db_pool(request: Request) -> AsyncConnectionPool | None:
    """Inject the PostgreSQL connection pool from app state."""
    return getattr(request.app.state, "db_pool", None)


def get_app_state(request: Request):
    """Inject the full app state for accessing service availability flags."""
    return request.app.state

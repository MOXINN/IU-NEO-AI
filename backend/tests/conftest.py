"""
IU NWEO AI — Test Configuration & Fixtures
Maintainer: Architect

Shared fixtures for all backend tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def app():
    """Create a fresh FastAPI app instance for testing."""
    from main import app as fastapi_app

    # Set test state defaults
    fastapi_app.state.db_pool = None
    fastapi_app.state.chroma_available = False
    fastapi_app.state.neo4j_available = False
    fastapi_app.state.semantic_router_available = False

    return fastapi_app


@pytest.fixture
def client(app):
    """Synchronous test client for non-streaming endpoints."""
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def mock_db_pool():
    """Mock async connection pool for PostgreSQL tests."""
    pool = AsyncMock()
    conn = AsyncMock()
    pool.connection.return_value.__aenter__ = AsyncMock(return_value=conn)
    pool.connection.return_value.__aexit__ = AsyncMock(return_value=False)
    conn.execute = AsyncMock()
    return pool


@pytest.fixture
def app_with_db(app, mock_db_pool):
    """App fixture with a mocked healthy DB pool."""
    app.state.db_pool = mock_db_pool
    return app


@pytest.fixture
def client_with_db(app_with_db):
    """Test client with mocked healthy DB."""
    return TestClient(app_with_db, raise_server_exceptions=False)

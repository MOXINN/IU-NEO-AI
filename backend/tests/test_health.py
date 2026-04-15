"""
IU NWEO AI — Health Endpoint Tests
Maintainer: Architect
"""


class TestHealthEndpoint:
    """Tests for GET /api/v1/health"""

    def test_health_returns_200(self, client):
        """Health endpoint should always return 200, even if services are down."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_has_required_fields(self, client):
        """Response should contain 'status' and 'services' keys."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "status" in data
        assert "services" in data

    def test_health_all_services_listed(self, client):
        """All four backing services should be reported."""
        response = client.get("/api/v1/health")
        services = response.json()["services"]
        assert "postgres" in services
        assert "chroma" in services
        assert "neo4j" in services
        assert "semantic_router" in services

    def test_health_degraded_when_no_db(self, client):
        """Status should be 'degraded' when PostgreSQL is unavailable."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["status"] in ("degraded", "operational")

    def test_health_services_unavailable_by_default(self, client):
        """With no services configured, all should report 'unavailable'."""
        response = client.get("/api/v1/health")
        services = response.json()["services"]
        assert services["postgres"] == "unavailable"
        assert services["chroma"] == "unavailable"
        assert services["neo4j"] == "unavailable"
        assert services["semantic_router"] == "unavailable"


class TestRootEndpoint:
    """Tests for GET /"""

    def test_root_returns_200(self, client):
        """Root endpoint should return service info."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_has_service_info(self, client):
        """Root should contain service name and version."""
        data = client.get("/").json()
        assert "service" in data
        assert "version" in data
        assert "status" in data

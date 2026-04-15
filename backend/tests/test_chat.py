"""
IU NWEO AI — Chat Endpoint Tests
Maintainer: Architect
"""


class TestChatEndpoint:
    """Tests for POST /api/v1/chat/stream"""

    def test_empty_message_returns_400(self, client):
        """Empty messages should be rejected with 400."""
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "", "thread_id": "test-thread"},
        )
        # Pydantic validation should catch min_length=1
        assert response.status_code in (400, 422)

    def test_whitespace_only_message_returns_400(self, client):
        """Whitespace-only messages should be rejected."""
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "   ", "thread_id": "test-thread"},
        )
        assert response.status_code in (400, 422)

    def test_missing_message_field_returns_422(self, client):
        """Missing required 'message' field should return 422."""
        response = client.post(
            "/api/v1/chat/stream",
            json={"thread_id": "test-thread"},
        )
        assert response.status_code == 422

    def test_valid_message_returns_200_sse(self, client):
        """A valid message should return a 200 SSE response."""
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "Hello", "thread_id": "test-thread"},
        )
        # SSE endpoints return 200 with text/event-stream content type
        assert response.status_code == 200

    def test_default_thread_id_when_missing(self, client):
        """When thread_id is not provided, it should default to 'default-thread'."""
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": "Hello"},
        )
        assert response.status_code == 200

    def test_message_too_long_returns_422(self, client):
        """Messages exceeding max_length should be rejected."""
        long_message = "x" * 5001
        response = client.post(
            "/api/v1/chat/stream",
            json={"message": long_message, "thread_id": "test-thread"},
        )
        assert response.status_code == 422

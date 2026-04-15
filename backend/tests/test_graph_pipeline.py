"""
IU NWEO AI — LangGraph Pipeline Unit Tests
Maintainer: Architect

Tests for individual LangGraph nodes and the routing logic.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage

from app.ai.graph.state import AgentState
from app.ai.graph.builder import route_intent


class TestRouteIntent:
    """Tests for the route_intent conditional edge function."""

    def test_low_confidence_routes_to_fallback(self):
        """Confidence below 0.6 should route to fallback."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "academic",
            "confidence": 0.3,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "fallback"

    def test_unknown_intent_routes_to_fallback(self):
        """Unknown intent should route to fallback."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "unknown",
            "confidence": 0.9,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "fallback"

    def test_academic_routes_to_vector(self):
        """Academic intent with high confidence should route to vector search."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "academic",
            "confidence": 0.8,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "vector"

    def test_administrative_routes_to_vector(self):
        """Administrative intent should route to vector search."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "administrative",
            "confidence": 0.85,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "vector"

    def test_greeting_routes_to_vector(self):
        """Greeting intent should route to vector search."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "greeting",
            "confidence": 0.95,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "vector"

    def test_prerequisite_routes_to_graph(self):
        """Prerequisite intent should route to graph search."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "prerequisite",
            "confidence": 0.88,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "graph"

    def test_missing_intent_defaults_to_fallback(self):
        """Missing intent key should default to fallback."""
        state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "intent": "",
            "confidence": 0.0,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        assert route_intent(state) == "fallback"


class TestFallbackNode:
    """Tests for the fallback node."""

    @pytest.mark.asyncio
    async def test_fallback_returns_ai_message(self):
        """Fallback should return an AIMessage in the messages list."""
        from app.ai.graph.nodes.fallback import fallback_node

        state: AgentState = {
            "messages": [HumanMessage(content="gibberish xyz")],
            "intent": "unknown",
            "confidence": 0.1,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        result = await fallback_node(state)
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
        assert result["search_type"] == "none"

    @pytest.mark.asyncio
    async def test_fallback_message_content(self):
        """Fallback message should contain helpful guidance."""
        from app.ai.graph.nodes.fallback import fallback_node

        state: AgentState = {
            "messages": [HumanMessage(content="xyz")],
            "intent": "unknown",
            "confidence": 0.0,
            "retrieved_context": "",
            "search_type": "none",
            "user_id": "test",
        }
        result = await fallback_node(state)
        content = result["messages"][0].content
        assert "sorry" in content.lower() or "trouble" in content.lower()


class TestSemanticRouter:
    """Tests for the semantic router fast-path."""

    def test_canned_responses_exist(self):
        """Canned responses should be defined for known routes."""
        from app.ai.routing.semantic_router import CANNED_RESPONSES

        assert "greeting" in CANNED_RESPONSES
        assert "faq_admission" in CANNED_RESPONSES
        assert len(CANNED_RESPONSES["greeting"]) > 0
        assert len(CANNED_RESPONSES["faq_admission"]) > 0


class TestAgentState:
    """Tests for the AgentState TypedDict structure."""

    def test_state_accepts_all_required_fields(self):
        """AgentState should accept all defined fields."""
        state: AgentState = {
            "messages": [HumanMessage(content="Hello")],
            "intent": "greeting",
            "retrieved_context": "Some context",
            "search_type": "vector",
            "confidence": 0.95,
            "user_id": "user-123",
        }
        assert state["intent"] == "greeting"
        assert state["confidence"] == 0.95

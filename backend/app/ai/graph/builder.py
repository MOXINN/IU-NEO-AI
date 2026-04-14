"""
IU NWEO AI — LangGraph Builder
Maintainer: Architect
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from app.ai.graph.state import AgentState

# Import nodes
from app.ai.graph.nodes.classify import classify_intent_node
from app.ai.graph.nodes.vector_search import vector_search_node
from app.ai.graph.nodes.graph_search import graph_search_node
from app.ai.graph.nodes.generate import generate_node
from app.ai.graph.nodes.fallback import fallback_node

def route_intent(state: AgentState) -> Literal["vector", "graph", "fallback"]:
    """
    Conditional edge routing logic.
    Determines next node based on classification intent and confidence.
    """
    intent = state.get("intent", "unknown")
    confidence = state.get("confidence", 0.0)

    # Route logic
    if confidence < 0.6 or intent == "unknown":
        return "fallback"
    
    if intent in ["academic", "administrative", "greeting"]:
        # Standard queries go to Vector DB
        return "vector"
    
    if intent in ["prerequisite"]:
        # Structural relationship queries go to Graph DB
        return "graph"
        
    return "fallback"

def build_graph() -> StateGraph:
    """
    Constructs the uncompiled StateGraph.
    """
    builder = StateGraph(AgentState)
    
    # 1. Add Nodes
    builder.add_node("classify", classify_intent_node)
    builder.add_node("vector_search", vector_search_node)
    builder.add_node("graph_search", graph_search_node)
    builder.add_node("generate_response", generate_node)
    builder.add_node("fallback_handler", fallback_node)
    
    # 2. Define standard edges
    # START -> classify -> routing -> (vector | graph | fallback) -> generate -> END
    builder.add_edge(START, "classify")
    
    # Conditional Edges from classify
    builder.add_conditional_edges(
        "classify",
        route_intent,
        {
            "vector": "vector_search",
            "graph": "graph_search",
            "fallback": "fallback_handler"
        }
    )
    
    # All retrieval routes lead to generator
    builder.add_edge("vector_search", "generate_response")
    builder.add_edge("graph_search", "generate_response")
    
    # Fallback and Generate lead to End
    builder.add_edge("fallback_handler", END)
    builder.add_edge("generate_response", END)
    
    return builder

# Compile without checkpointer for now - checkpointer will be attached in chat.py router
# where we have access to the async Postgres dependency injected by FastAPI.
uncompiled_graph = build_graph()

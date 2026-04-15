"""
IU NWEO AI — LangGraph Graph Search Node
Maintainer: Architect

Retrieves structured context from Neo4j (GraphRAG).
Falls back to a descriptive message if Neo4j is unavailable.
"""

import logging
from app.ai.graph.state import AgentState
from app.ai.rag.graph_store import search_graph_db

logger = logging.getLogger("iu-nweo.nodes.graph_search")


async def graph_search_node(state: AgentState) -> AgentState:
    """
    Retrieves structured context from Neo4j for relationship-based queries
    (e.g., course prerequisites, department structures).
    Gracefully degrades if Neo4j is unreachable.
    """
    query_text = state["messages"][-1].content

    try:
        context = await search_graph_db(query_text)
        logger.info(f"Graph search returned {len(context)} chars for: {query_text[:50]}...")
    except Exception as e:
        logger.warning(f"Neo4j search failed: {e}. Using fallback context.")
        context = (
            "[GRAPH SEARCH UNAVAILABLE]\n"
            "Neo4j is currently offline. Unable to query the course prerequisite graph. "
            "Please answer based on your general knowledge, but clearly state that "
            "prerequisite information could not be verified against the official graph."
        )

    return {
        "retrieved_context": context,
        "search_type": "graph",
    }

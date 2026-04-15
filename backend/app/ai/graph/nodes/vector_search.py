"""
IU NWEO AI — LangGraph Vector Search Node
Maintainer: Architect

Retrieves semantic context from ChromaDB.
Falls back to a descriptive message if ChromaDB is unavailable.
"""

import logging
from app.ai.graph.state import AgentState
from app.ai.rag.vector_store import search_vector_db

logger = logging.getLogger("iu-nweo.nodes.vector_search")


async def vector_search_node(state: AgentState) -> AgentState:
    """
    Retrieves semantic context from ChromaDB based on the user's query.
    Gracefully degrades if ChromaDB is unreachable.
    """
    query_text = state["messages"][-1].content

    try:
        context = await search_vector_db(query_text, top_k=4)
        logger.info(f"Vector search returned {len(context)} chars for: {query_text[:50]}...")
    except Exception as e:
        logger.warning(f"ChromaDB search failed: {e}. Using fallback context.")
        context = (
            "[VECTOR SEARCH UNAVAILABLE]\n"
            "ChromaDB is currently offline. Unable to retrieve university documents. "
            "Please answer based on your general knowledge about Integral University, "
            "but clearly state that the information could not be verified against official records."
        )

    return {
        "retrieved_context": context,
        "search_type": "vector",
    }

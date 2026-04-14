"""
IU NWEO AI — LangGraph Vector Search Node
Maintainer: Architect
"""

from app.ai.graph.state import AgentState

async def vector_search_node(state: AgentState) -> AgentState:
    """
    Retrieves semantic context from ChromaDB based on the query.
    Phase 2 stub: Returns placeholder context indicating standard RAG.
    """
    # TODO Phase 3: Add actual ChromaDB collection querying here
    query_text = state["messages"][-1].content
    
    mock_context = (
        f"[VECTOR RAG RESULTS for '{query_text}']\n"
        "- The University was founded to provide quality education.\n"
        "- All fees must be paid prior to the semester start.\n"
    )
    
    return {
        "retrieved_context": mock_context,
        "search_type": "vector"
    }

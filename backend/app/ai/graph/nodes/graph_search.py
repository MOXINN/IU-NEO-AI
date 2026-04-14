"""
IU NWEO AI — LangGraph Graph Search Node
Maintainer: Architect
"""

from app.ai.graph.state import AgentState

async def graph_search_node(state: AgentState) -> AgentState:
    """
    Retrieves structured context from Neo4j (GraphRAG).
    Phase 2 stub: Returns placeholder context for multi-hop graph questions.
    """
    # TODO Phase 3: Add actual Neo4j Cypher querying here
    query_text = state["messages"][-1].content
    
    mock_context = (
        f"[GRAPH RAG RESULTS for '{query_text}']\n"
        "(Course: CS101)-[:HAS_PREREQUISITE]->(Course: MATH101)\n"
        "(Program: Computer Science)-[:INCLUDES]->(Course: CS101)\n"
    )
    
    return {
        "retrieved_context": mock_context,
        "search_type": "graph"
    }

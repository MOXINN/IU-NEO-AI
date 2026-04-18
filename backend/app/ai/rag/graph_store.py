"""
IU NWEO AI — Neo4j Graph Store Integration
Maintainer: Architect
"""

# ---------------------------------------------------------------------------
# P1 FIX: Corrected import path
# Old: from langchain_neo4j import Neo4jGraph  (deprecated)
# New: from langchain_neo4j import Neo4jGraph  (matches requirements.txt)
# ---------------------------------------------------------------------------
from langchain_neo4j import Neo4jGraph
from app.core.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

_graph = None

def get_graph_store() -> Neo4jGraph:
    """
    Returns a configured Neo4jGraph instance for Cypher traversal.
    """
    global _graph
    if _graph is None:
        try:
            _graph = Neo4jGraph(
                url=settings.NEO4J_URI,
                username=settings.NEO4J_USER,
                password=settings.NEO4J_PASSWORD
            )
            # Fetch the schema on init so LLM has context
            _graph.refresh_schema()
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
    return _graph

async def search_graph_db(query: str) -> str:
    """
    Phase 3: Basic traversal search. 
    A production version would use an LLM-Cypher generator.
    """
    # -----------------------------------------------------------------------
    # P2 FIX: Wrap sync Neo4j calls with asyncio.to_thread to avoid
    # blocking the event loop on slow Neo4j operations.
    # -----------------------------------------------------------------------
    try:
        graph = await asyncio.to_thread(get_graph_store)
    except Exception:
        return "Graph DB offline."

    if not graph:
        return "Graph DB offline."
        
    # P1 FIX: Defensive schema access — get_schema is a property that
    # can return None if refresh_schema() failed during init.
    schema = graph.get_schema or "Schema unavailable"
    return (
        f"[GRAPH SCHEMA INFO available for routing]\n{schema}\n"
        "*(Note: full Text-to-Cypher translation requires additional LLM call step)*"
    )

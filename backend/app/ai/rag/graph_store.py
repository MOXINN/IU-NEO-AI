"""
IU NWEO AI — Neo4j Graph Store Integration
Maintainer: Architect
"""

from langchain_community.graphs import Neo4jGraph
from app.core.config import settings
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
            # Fetch the schema asynchronously or on init so LLM has context
            _graph.refresh_schema()
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
    return _graph

async def search_graph_db(query: str) -> str:
    """
    Phase 3: Basic traversal search. 
    A production version would use an LLM-Cypher generator.
    """
    graph = get_graph_store()
    if not graph:
        return "Graph DB offline."
        
    # In a full setup, we would use `GraphCypherQAChain` here to generate cypher
    # based on the query. For the baseline Enterprise setup, we simulate a fast path:
    
    # This is a generic return assuming the graph holds structural relationships.
    # We will refine the GraphRAG capability with `neo4j-graphrag` later if needed.
    schema = graph.get_schema
    return f"[GRAPH SCHEMA INFO available for routing]\n{schema}\n*(Note: full Text-to-Cypher translation requires additional LLM call step)*"

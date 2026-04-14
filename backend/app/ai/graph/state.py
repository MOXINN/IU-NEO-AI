"""
IU NWEO AI — LangGraph State Definition
Maintainer: Architect
"""

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The central state object that is passed around between all nodes in the Graph.
    This state gets checkpointed into PostgreSQL automatically by LangGraph's 
    AsyncPostgresSaver, keyed by `thread_id`.
    """
    # Messages list uses the `add_messages` reducer to automatically append new messages.
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Metadata for the current interaction step
    intent: str               # "academic", "administrative", "prerequisite", "greeting", "unknown"
    retrieved_context: str    # Raw text or concatenated chunks from RAG
    search_type: str          # "vector" for ChromaDB, "graph" for Neo4j, "none"
    confidence: float         # 0.0 to 1.0 confidence score from the classifier node
    user_id: str              # the UUID/Identifier of the current user, useful for analytics later

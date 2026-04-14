"""
IU NWEO AI — LangGraph Fallback Node
Maintainer: Architect
"""

from langchain_core.messages import AIMessage
from app.ai.graph.state import AgentState

async def fallback_node(state: AgentState) -> AgentState:
    """
    Provides a safe response when intent classification fails or confidence is too low.
    Injects an AIMessage directly to end the flow.
    """
    response_text = (
        "I'm sorry, I'm having trouble understanding that request. "
        "I am best equipped to help with queries about courses, prerequisites, and admissions."
    )
    
    msg = AIMessage(content=response_text)
    
    return {
        "messages": [msg],
        "search_type": "none"
    }

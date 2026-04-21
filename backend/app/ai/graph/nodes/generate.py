"""
IU NWEO AI — LangGraph Generate Node
Maintainer: Architect
"""

from langchain_core.messages import SystemMessage
from app.ai.models.gemini import get_gemini_pro_model
from app.ai.graph.state import AgentState

# ---------------------------------------------------------------------------
# P0 FIX: Lazy LLM initialization
# ---------------------------------------------------------------------------
_stream_llm = None


def _get_stream_llm():
    global _stream_llm
    if _stream_llm is None:
        _stream_llm = get_gemini_pro_model(temperature=0.2, streaming=True)
    return _stream_llm

GENERATE_SYSTEM_PROMPT = """You are the official AI Assistant for Integral University.
You are a helpful, proactive university peer.

INSTRUCTIONS:
1. Priority: Use the [RETRIEVED CONTEXT] provided below to answer the user's question accurately.
2. Flexibility: If the information is not explicitly in the context but relates to general university knowledge (e.g., Integral University is in Lucknow, its reputation, standard campus protocols like IUET), you MUST provide a helpful response based on your internal knowledge.
3. Disclaimer: If you use internal knowledge not found in the context, clearly state that this is general information and suggest the user verify it with the official university website or admissions office.
4. Transparency: Always cite the source if it comes from the provided context (e.g., "[Source: Document]").
5. Search Mode: You are currently using the {search_type} search method.

--- RETRIEVED CONTEXT ---
{context}
-------------------------
"""

async def generate_node(state: AgentState) -> AgentState:
    """
    Generates the final response using streaming Gemini and the retrieved 
    context from either vector or graph storage.
    """
    
    context = state.get("retrieved_context", "No context provided.")
    search_type = state.get("search_type", "unknown")
    
    sys_msg = SystemMessage(
        content=GENERATE_SYSTEM_PROMPT.format(search_type=search_type, context=context)
    )
    
    # We pass the system prompt followed by all interaction messages to retain conversation history
    messages_for_llm = [sys_msg] + list(state["messages"])
    
    # The astream_events engine requires us to invoke it, but inside a node
    # returning an ainvoke result will yield correctly to the graph stream.
    response = await _get_stream_llm().ainvoke(messages_for_llm)
    
    # We return the response as an AIMessage to append to the state's message list.
    return {"messages": [response]}

"""
IU NWEO AI — LangGraph Generate Node
Maintainer: Architect
"""

from langchain_core.messages import SystemMessage
from app.ai.models.gemini import get_gemini_pro_model
from app.ai.graph.state import AgentState

# Must be streaming=True for astream_events to work dynamically token by token
stream_llm = get_gemini_pro_model(temperature=0.2, streaming=True)

GENERATE_SYSTEM_PROMPT = """You are the official AI Assistant for Integral University.
You are professional, concise, and highly accurate.
You must use the provided context below to answer the user's question.
If the answer is not in the context, do not make it up—simply state you do not have the information.

Search Method Used: {search_type}

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
    response = await stream_llm.ainvoke(messages_for_llm)
    
    # We return the response as an AIMessage to append to the state's message list.
    return {"messages": [response]}

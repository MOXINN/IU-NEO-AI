"""
IU NWEO AI — Chat Route with LangGraph Streaming
Maintainer: Architect
"""

import json
import asyncio
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import MemorySaver

from app.ai.graph.builder import uncompiled_graph
from app.ai.routing.semantic_router import check_fast_route, CANNED_RESPONSES

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default-thread"

async def generate_chat_stream(request: Request, user_message: str, thread_id: str):
    """
    Asynchronous generator yielding SSE chunks from the LangGraph execution.
    Utilizes astream_events to send token-by-token updates and state changes.
    """
    # --- PHASE 4: Semantic Router Fast Path ---
    fast_route_name = check_fast_route(user_message)
    if fast_route_name and fast_route_name in CANNED_RESPONSES:
        logger.info(f"Semantic Router match: {fast_route_name}. Bypassing LLM.")
        canned_text = CANNED_RESPONSES[fast_route_name]
        # Yield status
        yield {"event": "status", "data": "Instant Match found."}
        await asyncio.sleep(0.01)
        # Yield text
        yield {"event": "message", "data": canned_text}
        yield {"event": "done", "data": "[DONE]"}
        return
    # --- END Semantic Router ---

    db_pool = getattr(request.app.state, "db_pool", None)
    
    if db_pool:
        checkpointer = AsyncPostgresSaver(db_pool)
        # Setup creates the required DB tables (idempotent)
        await checkpointer.setup()
        graph = uncompiled_graph.compile(checkpointer=checkpointer)
    else:
        # Fallback to in-memory if DB is unavailable
        logger.warning("Using MemorySaver since db_pool is unavailable.")
        checkpointer = MemorySaver()
        graph = uncompiled_graph.compile(checkpointer=checkpointer)
        
    config = {"configurable": {"thread_id": thread_id}}
    input_data = {"messages": [HumanMessage(content=user_message)]}
    
    try:
        # astream_events(..., version="v2") provides granular events
        async for event in graph.astream_events(input_data, config=config, version="v2"):
            if await request.is_disconnected():
                logger.info(f"Client disconnected for thread {thread_id}")
                break

            kind = event["event"]
            node = event.get("metadata", {}).get("langgraph_node", "unknown")
            
            # --- Stream LLM Tokens ---
            # We look for chat model streaming events inside the 'generate_response' node.
            # In LangGraph v2 and LangChain v0.3, chat models emit on_chat_model_stream.
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield {
                        "event": "message",
                        "data": content
                    }
                    await asyncio.sleep(0.01) # Yield control
            
            # --- Stream Node Transitions (Status Updates) ---
            elif kind == "on_node_start":
                # Push a status update to the client indicating what the AI is currently doing
                status_msg = ""
                if node == "classify":
                    status_msg = "Classifying query..."
                elif node == "vector_search":
                    status_msg = "Searching academic records..."
                elif node == "graph_search":
                    status_msg = "Exploring prerequisites graph..."
                elif node == "fallback_handler":
                    status_msg = "Falling back to safe defaults..."
                
                if status_msg:
                    yield {
                        "event": "status",
                        "data": status_msg
                    }
            
            elif kind == "on_node_end":
                # For debugging/UX purposes, we tell the frontend that a node finished.
                # If we just finished classification, we might want to expose the routing choice
                pass

        # Send completion signal
        yield {
            "event": "done",
            "data": "[DONE]"
        }
        
    except Exception as e:
        logger.error(f"Streaming error: {e}", exc_info=True)
        yield {
            "event": "error",
            "data": str(e)
        }

@router.post("/stream")
async def chat_stream_endpoint(request: Request, payload: ChatRequest):
    """
    SSE stream endpoint for the Next.js frontend.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    return EventSourceResponse(generate_chat_stream(request, payload.message, payload.thread_id))
"""
IU NWEO AI — Chat Service
Maintainer: Architect

Business logic for chat orchestration:
  1. Check Semantic Router fast-path
  2. Compile LangGraph with checkpointer (cached)
  3. Stream events back as SSE
"""

import asyncio
import logging
from typing import AsyncGenerator, Dict, Any

from fastapi import Request
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from app.ai.graph.builder import uncompiled_graph
from app.ai.routing.semantic_router import check_fast_route, CANNED_RESPONSES

logger = logging.getLogger("iu-nweo.services.chat")


async def try_fast_route(message: str, request: Request) -> str | None:
    """
    Attempt Semantic Router fast match.
    Returns canned response if matched, None otherwise.
    Fails silently if the router isn't available.
    """
    semantic_router_ok = getattr(request.app.state, "semantic_router_available", False)
    if not semantic_router_ok:
        return None

    try:
        route_name = check_fast_route(message)
        if route_name and route_name in CANNED_RESPONSES:
            logger.info(f"Semantic Router match: {route_name}. Bypassing LLM.")
            return CANNED_RESPONSES[route_name]
    except Exception as e:
        logger.warning(f"Semantic Router check failed: {e}")

    return None


async def get_compiled_graph(request: Request):
    """
    Returns a compiled LangGraph StateGraph with the appropriate checkpointer.

    P1 FIX: No longer calls checkpointer.setup() here — that moved to lifespan.
    P2 FIX: Caches the compiled graph on app.state so we don't recompile every request.
            Graph compilation is deterministic for a given checkpointer instance.
    """
    # Return cached graph if available
    cached = getattr(request.app.state, "_compiled_graph", None)
    if cached is not None:
        return cached

    # Use the pre-initialized checkpointer from lifespan, or fall back to MemorySaver
    checkpointer = getattr(request.app.state, "checkpointer", None)

    if checkpointer:
        graph = uncompiled_graph.compile(checkpointer=checkpointer)
    else:
        logger.warning("Using MemorySaver since db_pool is unavailable.")
        graph = uncompiled_graph.compile(checkpointer=MemorySaver())

    # Cache for subsequent requests
    request.app.state._compiled_graph = graph
    return graph


async def generate_chat_stream(
    request: Request,
    user_message: str,
    thread_id: str,
) -> AsyncGenerator[Dict[str, str], None]:
    """
    Core streaming generator. Yields SSE-formatted dicts:
      {"event": "status|message|done|error", "data": "..."}
    """
    # --- Fast Path: Semantic Router ---
    canned = await try_fast_route(user_message, request)
    if canned:
        yield {"event": "status", "data": "Instant Match found."}
        await asyncio.sleep(0.01)
        yield {"event": "message", "data": canned}
        yield {"event": "done", "data": "[DONE]"}
        return

    # --- Full Path: LangGraph ---
    try:
        graph = await get_compiled_graph(request)
    except Exception as e:
        logger.error(f"Graph compilation failed: {e}", exc_info=True)
        yield {"event": "error", "data": f"Failed to initialize AI pipeline: {e}"}
        return

    config = {"configurable": {"thread_id": thread_id}}
    input_data = {"messages": [HumanMessage(content=user_message)]}

    try:
        async for event in graph.astream_events(input_data, config=config, version="v2"):
            if await request.is_disconnected():
                logger.info(f"Client disconnected for thread {thread_id}")
                break

            kind = event["event"]
            node = event.get("metadata", {}).get("langgraph_node", "unknown")

            # --- Stream LLM Tokens ---
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield {"event": "message", "data": content}
                    await asyncio.sleep(0.01)

            # --- Stream Node Transitions (Status Updates) ---
            elif kind == "on_node_start":
                status_map = {
                    "classify": "Classifying query...",
                    "vector_search": "Searching academic records...",
                    "graph_search": "Exploring prerequisites graph...",
                    "fallback_handler": "Falling back to safe defaults...",
                    "generate_response": "Generating response...",
                }
                status_msg = status_map.get(node)
                if status_msg:
                    yield {"event": "status", "data": status_msg}

        # Send completion signal
        yield {"event": "done", "data": "[DONE]"}

    except Exception as e:
        logger.error(f"Streaming error: {e}", exc_info=True)
        yield {"event": "error", "data": str(e)}

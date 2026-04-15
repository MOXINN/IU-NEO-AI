"""
IU NWEO AI — Chat Route
Maintainer: Architect

Thin controller — validates input and delegates to chat_service.
"""

import logging
from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from app.models.chat import ChatRequest
from app.services.chat_service import generate_chat_stream

logger = logging.getLogger("iu-nweo.routes.chat")
router = APIRouter()


@router.post("/stream")
async def chat_stream_endpoint(request: Request, payload: ChatRequest):
    """
    SSE stream endpoint for the Next.js frontend.
    Validates input, then delegates streaming to the chat service.
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return EventSourceResponse(
        generate_chat_stream(request, payload.message, payload.thread_id)
    )
"""
IU NWEO AI — Chat DTOs
Maintainer: Architect

Pydantic models for the chat endpoint request/response contracts.
"""

from pydantic import BaseModel, Field
from enum import Enum


class ChatRequest(BaseModel):
    """Incoming chat request from the frontend."""
    message: str = Field(..., min_length=1, max_length=5000, description="User's chat message")
    thread_id: str = Field(default="default-thread", description="Conversation thread ID for state persistence")


class SSEEventType(str, Enum):
    """Types of events sent over the SSE stream."""
    STATUS = "status"
    MESSAGE = "message"
    DONE = "done"
    ERROR = "error"


class ChatStreamEvent(BaseModel):
    """Individual SSE event in the chat stream."""
    event: SSEEventType
    data: str

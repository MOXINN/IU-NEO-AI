"""
IU NWEO AI — Custom Exception Classes
Maintainer: Architect

Centralized error hierarchy. All exceptions carry a status_code and error_code
so the global exception handler in middleware.py can return structured JSON.
"""

from fastapi import status


class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred.",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)


class ValidationError(AppError):
    """Raised when request data fails validation."""

    def __init__(self, detail: str = "Validation error."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
        )


class LLMError(AppError):
    """Raised when the LLM (Gemini) call fails."""

    def __init__(self, detail: str = "LLM service unavailable."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="LLM_ERROR",
        )


class RAGError(AppError):
    """Raised when a RAG retrieval operation fails (ChromaDB / Neo4j)."""

    def __init__(self, detail: str = "RAG retrieval failed."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="RAG_ERROR",
        )


class DatabaseError(AppError):
    """Raised when PostgreSQL operations fail."""

    def __init__(self, detail: str = "Database operation failed."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="DATABASE_ERROR",
        )


class StreamingError(AppError):
    """Raised when SSE streaming encounters an unrecoverable issue."""

    def __init__(self, detail: str = "Streaming error."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="STREAMING_ERROR",
        )

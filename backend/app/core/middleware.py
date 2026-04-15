"""
IU NWEO AI — Middleware
Maintainer: Architect

Global exception handler and request lifecycle logging.
"""

import time
import uuid
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.errors import AppError

logger = logging.getLogger("iu-nweo.middleware")


def register_middleware(app: FastAPI) -> None:
    """Attach all middleware and exception handlers to the FastAPI app."""

    # --- Global Exception Handler ---
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.error(
            f"AppError [{exc.error_code}] {exc.status_code}: {exc.detail}",
            extra={"path": request.url.path},
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "error_code": exc.error_code,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            f"Unhandled exception on {request.method} {request.url.path}",
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "error_code": "INTERNAL_ERROR",
                "detail": "An unexpected error occurred. Please try again.",
            },
        )

    # --- Request Logging Middleware ---
    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        start_time = time.perf_counter()

        logger.info(
            f"[{request_id}] → {request.method} {request.url.path}"
        )

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"[{request_id}] ← {response.status_code} ({duration_ms:.0f}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        return response

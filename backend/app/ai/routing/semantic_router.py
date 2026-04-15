"""
IU NWEO AI — Semantic Router integration
Maintainer: Architect

Uses FastEmbed (ONNX) for sub-millisecond intent matching.
Provides instant canned responses for known fast-path queries,
bypassing the full LangGraph pipeline entirely.

The router initialization downloads a small ONNX model on first run.
All failures are caught gracefully — if the router breaks, queries
simply fall through to the full LangGraph pipeline.
"""

import logging
from semantic_router import Route, SemanticRouter
from semantic_router.encoders import FastEmbedEncoder

logger = logging.getLogger("iu-nweo.routing")

# Define routes for instant matching
greeting = Route(
    name="greeting",
    utterances=["hello", "hi", "hey", "good morning", "how are you"]
)

faq_admission = Route(
    name="faq_admission",
    utterances=[
        "how to apply", "when do admissions start",
        "admission process", "how to get into university"
    ]
)

# Shared router instance
_router = None
_init_failed = False


def get_route_layer() -> SemanticRouter | None:
    """
    Initializes and returns the semantic router.
    Returns None if initialization has previously failed to avoid repeated errors.
    """
    global _router, _init_failed

    if _init_failed:
        return None

    if _router is None:
        try:
            logger.info("Initializing FastEmbed encoder for Semantic Router...")
            encoder = FastEmbedEncoder()
            _router = SemanticRouter(encoder=encoder, routes=[greeting, faq_admission])
            logger.info("Semantic Router ready.")
        except Exception as e:
            logger.error(f"Semantic Router initialization failed: {e}")
            _init_failed = True
            return None

    return _router


def check_fast_route(query: str) -> str | None:
    """
    Evaluates the query against Semantic Router.
    Returns route name if matched, otherwise None.
    Returns None on any error (non-blocking).
    """
    try:
        router = get_route_layer()
        if router is None:
            return None
        route_choice = router(query)
        return route_choice.name if route_choice.name else None
    except Exception as e:
        logger.warning(f"Semantic Router query failed: {e}")
        return None


# Pre-computed Canned Responses for fast paths
CANNED_RESPONSES = {
    "greeting": (
        "Hello! I am the Integral University Agentic AI. "
        "How can I help you today? Ask me about courses, fees, or prerequisites."
    ),
    "faq_admission": (
        "Admissions typically begin in May. You can apply directly through "
        "the Integral University official admissions website."
    ),
}

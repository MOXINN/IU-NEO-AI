"""
IU NWEO AI — Semantic Router integration
Maintainer: Architect
"""

from semantic_router import Route
from semantic_router.layer import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder
import logging

logger = logging.getLogger(__name__)

# Define routes for instant matching
greeting = Route(
    name="greeting",
    utterances=["hello", "hi", "hey", "good morning", "how are you"]
)

faq_admission = Route(
    name="faq_admission",
    utterances=["how to apply", "when do admissions start", "admission process", "how to get into university"]
)

# Shared layer
_route_layer = None

def get_route_layer() -> RouteLayer:
    """Initializes and returns the semantic routing layer."""
    global _route_layer
    if _route_layer is None:
        logger.info("Initializing HuggingFace encoder for Semantic Router...")
        # Using a fast local encoder so we don't need OpenAI tokens for basic intents
        encoder = HuggingFaceEncoder(name="all-MiniLM-L6-v2")
        _route_layer = RouteLayer(encoder=encoder, routes=[greeting, faq_admission])
        logger.info("Semantic Router ready.")
    
    return _route_layer

def check_fast_route(query: str):
    """
    Evaluates the query against Semantic Router.
    Returns Route object if matched, otherwise None.
    """
    layer = get_route_layer()
    route_choice = layer(query)
    
    return route_choice.name if route_choice.name else None

# Pre-computed Canned Responses for fast paths
CANNED_RESPONSES = {
    "greeting": "Hello! I am the Integral University Agentic AI. How can I help you today? Ask me about courses, fees, or prerequisites.",
    "faq_admission": "Admissions typically begin in May. You can apply directly through the Integral University official admissions website."
}

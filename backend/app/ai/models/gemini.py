"""
IU NWEO AI — Gemini Model Configuration (2026 Stable)
Maintainer: Architect

Updated to use gemini-2.5-flash to resolve 404 NOT_FOUND errors
caused by the retirement of older 1.5 and 2.0 model names.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_gemini_pro_model(temperature: float = 0.2, streaming: bool = True):
    """
    Initializes the Gemini model using the current 2026 stable production names.
    Priority: gemini-2.5-flash -> gemini-2.5-flash-lite
    """
    
    # gemini-2.5-flash is the primary stable model for 2026
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        streaming=streaming,
        max_retries=3,          # Automatically retry on minor network flickers
        timeout=30,             # Prevent the "Establishing connection" hang
    )
    
    # fallback to the lite version if available (highly efficient for 2026 workloads)
    fallback_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        streaming=streaming,
        max_retries=3,
        timeout=30,
    )
    
    # Chain them so the system is highly resilient to quota limits or downtime
    return primary_llm.with_fallbacks([fallback_llm])
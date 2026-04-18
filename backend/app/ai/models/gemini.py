from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_gemini_pro_model(temperature: float = 0.2, streaming: bool = True):
    """
    Initializes and returns the Gemini model.
    Uses gemini-2.5-pro (2026 standard) with a fallback to gemini-2.0-flash.
    """
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        streaming=streaming
    )
    
    fallback_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        streaming=streaming
    )
    
    return primary_llm.with_fallbacks([fallback_llm])
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_gemini_pro_model(temperature: float = 0.2, streaming: bool = True) -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Gemini model.
    Uses gemini-1.5-pro for advanced reasoning and multimodal capabilities.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        streaming=streaming
    )
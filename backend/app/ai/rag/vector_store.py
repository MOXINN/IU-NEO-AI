"""
IU NWEO AI — ChromaDB Vector Store integration
Maintainer: Architect
"""

import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

# Shared initialized instances
_chroma_client = None
_vector_store = None

def get_chroma_client() -> chromadb.HttpClient:
    """Gets or initializes the global Chroma HTTP client."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
    return _chroma_client

def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",  # <--- THE FINAL FIX
        google_api_key=settings.GEMINI_API_KEY
    )

def get_vector_store(collection_name: str = "iu_knowledge") -> Chroma:
    """Returns a LangChain Chroma vector store instance connected to the persistent HTTP DB."""
    global _vector_store
    
    # We only initialize once per collection
    if _vector_store is None:
        client = get_chroma_client()
        embeddings = get_embeddings()
        
        _vector_store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )
    return _vector_store

async def search_vector_db(query: str, top_k: int = 3) -> str:
    """
    Semantic search used by LangGraph vector node.
    Returns formatted context string.
    """
    store = get_vector_store()
    # Using similarity search (could upgrade to MMR later if needed)
    docs = await store.asimilarity_search(query, k=top_k)
    
    if not docs:
        return "[SYSTEM: No specific documents found for this query in the knowledge base. Please rely on general university knowledge if applicable.]"
        
    context = "\n---\n".join([d.page_content for d in docs])
    return f"[VECTOR RAG RESULTS]\n{context}"
"""
IU NWEO AI — Document Loading and Chunking
Maintainer: Architect
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_dummy_data() -> list[Document]:
    """
    Simulates loading PDF/Text data about the University for initial seeding.
    In production, use PyPDFLoader or Unstructured.
    """
    text = (
        "Integral University is situated in Lucknow, UP. "
        "The computer science department offers B.Tech and M.Tech programs. "
        "The admission process starts in May every year. "
        "The library is located in the central block, open 24/7 during exams. "
        "To graduate, a student must complete 160 credits for B.Tech."
    )
    
    docs = [Document(page_content=text, metadata={"source": "university_handbook.txt"})]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    
    return splitter.split_documents(docs)

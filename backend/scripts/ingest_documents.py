"""
IU NWEO AI — ChromaDB Ingestion Script
Maintainer: Architect

Usage (from backend/):
    python -m scripts.ingest_documents

Seeds ChromaDB with university knowledge documents.
Requires ChromaDB to be running (docker compose up chroma).
"""

import sys
import os

# Ensure the backend root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.ai.rag.vector_store import get_vector_store
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============================================================================
# University Knowledge Base — Seed Data
# ============================================================================
# In production, replace this with PDF/DOCX loaders pointed at real documents.
# Each entry simulates a section from a university handbook or website.
# ============================================================================

UNIVERSITY_DOCUMENTS = [
    {
        "content": """Integral University (IU) is a prestigious institution located in Lucknow, 
Uttar Pradesh, India. Established in 2004, it is recognized by UGC and approved by AICTE. 
The university offers undergraduate, postgraduate, and doctoral programs across multiple 
faculties including Engineering, Science, Management, Law, Architecture, and Pharmacy. 
The campus spans over 105 acres with state-of-the-art laboratories, a central library, 
sports facilities, and separate hostels for male and female students.""",
        "metadata": {"source": "university_overview.pdf", "department": "general", "doc_type": "overview"}
    },
    {
        "content": """The Department of Computer Science and Engineering offers B.Tech (CSE), 
M.Tech (CSE), and Ph.D. programs. The B.Tech program requires completion of 160 credits 
over 8 semesters. Core subjects include Data Structures, Algorithms, Database Management 
Systems, Operating Systems, Computer Networks, and Software Engineering. Electives include 
Artificial Intelligence, Machine Learning, Cloud Computing, Cybersecurity, and Blockchain 
Technology. The department has 35 faculty members and 12 specialized labs including an 
AI/ML Research Lab, Cybersecurity Lab, and IoT Innovation Center.""",
        "metadata": {"source": "cse_handbook.pdf", "department": "CSE", "doc_type": "academic"}
    },
    {
        "content": """Admission to undergraduate programs at Integral University is based on 
entrance examination scores (JEE Main / university entrance test) and merit. The admission 
window opens in May and closes in July each year. Required documents include: 10th and 12th 
mark sheets, transfer certificate, character certificate, Aadhaar card, passport-size 
photographs, and entrance exam scorecard. International students can apply through the 
International Admissions Office with TOEFL/IELTS scores. A non-refundable application fee 
of INR 1,500 is required.""",
        "metadata": {"source": "admissions_guide.pdf", "department": "admissions", "doc_type": "administrative"}
    },
    {
        "content": """Fee structure for B.Tech programs (2024-2025): Tuition fee is INR 85,000 
per semester. Hostel fee is INR 45,000 per semester (including mess charges). Lab fee is 
INR 10,000 per semester. Exam fee is INR 3,000 per semester. Total approximate cost per 
semester is INR 1,43,000. Scholarships are available based on entrance exam rank (top 100: 
50% tuition waiver, top 500: 25% tuition waiver). Merit-based scholarships are renewed 
annually based on CGPA (minimum 8.0 required). Financial aid and education loans are 
facilitated through the university's tie-ups with nationalized banks.""",
        "metadata": {"source": "fee_structure.pdf", "department": "finance", "doc_type": "administrative"}
    },
    {
        "content": """The Central Library at Integral University houses over 1,50,000 books, 
5,000 journals, and provides access to digital databases including IEEE Xplore, Springer, 
Scopus, and Web of Science. The library operates from 8:00 AM to 10:00 PM on regular days 
and is open 24/7 during examination periods. Students can borrow up to 4 books at a time 
for a period of 14 days. The library also has a dedicated reading hall with 500 seats, 
a digital resource center with 100 computer terminals, and group discussion rooms.""",
        "metadata": {"source": "library_guide.pdf", "department": "library", "doc_type": "facilities"}
    },
    {
        "content": """Integral University placement cell has maintained a strong record with 
an average placement rate of 78% for the 2023-24 batch. Major recruiters include TCS, 
Infosys, Wipro, HCL, Cognizant, Capgemini, Accenture, Amazon, and Microsoft. The highest 
package offered was INR 42 LPA (Amazon) and the average package was INR 5.2 LPA. The 
placement cell organizes pre-placement training, mock interviews, resume workshops, and 
aptitude test preparation starting from the 5th semester.""",
        "metadata": {"source": "placement_report.pdf", "department": "placements", "doc_type": "career"}
    },
    {
        "content": """The university campus has a fully equipped medical center with a 
resident doctor available 24/7. Transportation is provided through a fleet of 25 buses 
covering routes across Lucknow and surrounding areas. The campus has a canteen, a cafeteria, 
and a food court. Sports facilities include a cricket ground, football field, basketball 
court, badminton courts, gymnasium, and swimming pool. Cultural events are organized 
throughout the year, with the annual cultural fest 'Technotron' being the flagship event.""",
        "metadata": {"source": "campus_facilities.pdf", "department": "administration", "doc_type": "facilities"}
    },
    {
        "content": """Research at Integral University is coordinated through the Directorate 
of Research. The university has published over 3,500 research papers in indexed journals. 
Active research areas include Artificial Intelligence, Renewable Energy, Nanotechnology, 
Pharmaceutical Sciences, and Environmental Science. The university has received grants 
from DST, SERB, UGC, ICSSR, and CSIR. Faculty members can apply for internal research 
seed grants of up to INR 5 lakhs. Ph.D. scholars receive a monthly stipend of INR 25,000 
for the first two years.""",
        "metadata": {"source": "research_brochure.pdf", "department": "research", "doc_type": "academic"}
    },
]


def run_ingestion():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("IU NWEO AI — ChromaDB Document Ingestion")
    print("=" * 60)

    # Build Document objects
    docs = []
    for entry in UNIVERSITY_DOCUMENTS:
        docs.append(Document(
            page_content=entry["content"].strip(),
            metadata=entry["metadata"]
        ))

    print(f"Loaded {len(docs)} raw documents.")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    # Upsert into ChromaDB
    print("Connecting to ChromaDB...")
    store = get_vector_store(collection_name="iu_knowledge")

    print("Adding documents to collection 'iu_knowledge'...")
    store.add_documents(chunks)

    print(f"✓ Successfully ingested {len(chunks)} chunks into ChromaDB.")
    print("=" * 60)


if __name__ == "__main__":
    run_ingestion()

"""
IU NWEO AI — Neo4j Knowledge Graph Seed Script
Maintainer: Architect

Usage (from backend/):
    python -m scripts.seed_neo4j

Seeds Neo4j with structured university data: departments, courses,
faculty, programs, and relationships (prerequisites, teaches, belongs_to).
Requires Neo4j to be running (docker compose up neo4j).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from neo4j import GraphDatabase
from app.core.config import settings


# ============================================================================
# Cypher statements to build the Knowledge Graph
# ============================================================================

SEED_CYPHER = [
    # --- Clear existing data (for re-runs) ---
    "MATCH (n) DETACH DELETE n",

    # --- Departments ---
    """
    CREATE (:Department {name: 'Computer Science and Engineering', code: 'CSE', hod: 'Dr. Raees Ahmad Khan'})
    CREATE (:Department {name: 'Electronics and Communication', code: 'ECE', hod: 'Dr. Mohd Wajid'})
    CREATE (:Department {name: 'Mechanical Engineering', code: 'ME', hod: 'Dr. Aas Mohammad'})
    CREATE (:Department {name: 'Civil Engineering', code: 'CE', hod: 'Dr. Sabih Ahmad'})
    CREATE (:Department {name: 'Pharmacy', code: 'PHARM', hod: 'Dr. Mohammad Amir'})
    CREATE (:Department {name: 'Management Studies', code: 'MBA', hod: 'Dr. Syed Husain Ashraf'})
    """,

    # --- Programs ---
    """
    CREATE (:Program {name: 'B.Tech Computer Science', code: 'BTECH-CSE', degree_type: 'Undergraduate', duration_years: 4, total_credits: 160})
    CREATE (:Program {name: 'M.Tech Computer Science', code: 'MTECH-CSE', degree_type: 'Postgraduate', duration_years: 2, total_credits: 80})
    CREATE (:Program {name: 'B.Tech Electronics', code: 'BTECH-ECE', degree_type: 'Undergraduate', duration_years: 4, total_credits: 160})
    CREATE (:Program {name: 'MBA', code: 'MBA', degree_type: 'Postgraduate', duration_years: 2, total_credits: 90})
    CREATE (:Program {name: 'B.Pharm', code: 'BPHARM', degree_type: 'Undergraduate', duration_years: 4, total_credits: 150})
    """,

    # --- CSE Courses ---
    """
    CREATE (:Course {name: 'Introduction to Programming', code: 'CS101', credits: 4, semester: 1, type: 'core'})
    CREATE (:Course {name: 'Mathematics I', code: 'MATH101', credits: 4, semester: 1, type: 'core'})
    CREATE (:Course {name: 'Data Structures', code: 'CS201', credits: 4, semester: 3, type: 'core'})
    CREATE (:Course {name: 'Algorithms', code: 'CS301', credits: 4, semester: 4, type: 'core'})
    CREATE (:Course {name: 'Database Management Systems', code: 'CS302', credits: 4, semester: 4, type: 'core'})
    CREATE (:Course {name: 'Operating Systems', code: 'CS303', credits: 4, semester: 5, type: 'core'})
    CREATE (:Course {name: 'Computer Networks', code: 'CS401', credits: 4, semester: 5, type: 'core'})
    CREATE (:Course {name: 'Software Engineering', code: 'CS402', credits: 3, semester: 6, type: 'core'})
    CREATE (:Course {name: 'Artificial Intelligence', code: 'CS501', credits: 4, semester: 6, type: 'elective'})
    CREATE (:Course {name: 'Machine Learning', code: 'CS502', credits: 4, semester: 7, type: 'elective'})
    CREATE (:Course {name: 'Cloud Computing', code: 'CS503', credits: 3, semester: 7, type: 'elective'})
    CREATE (:Course {name: 'Cybersecurity', code: 'CS504', credits: 3, semester: 7, type: 'elective'})
    CREATE (:Course {name: 'Deep Learning', code: 'CS601', credits: 4, semester: 8, type: 'elective'})
    """,

    # --- Faculty ---
    """
    CREATE (:Faculty {name: 'Dr. Raees Ahmad Khan', title: 'Professor & HOD', specialization: 'Cybersecurity'})
    CREATE (:Faculty {name: 'Dr. Mohammad Amjad', title: 'Associate Professor', specialization: 'AI/ML'})
    CREATE (:Faculty {name: 'Dr. Tanvir Ahmad', title: 'Associate Professor', specialization: 'NLP'})
    CREATE (:Faculty {name: 'Dr. Mohd Haroon', title: 'Assistant Professor', specialization: 'Cloud Computing'})
    CREATE (:Faculty {name: 'Dr. Khaleel Ahmad', title: 'Professor', specialization: 'Cryptography'})
    """,

    # --- RELATIONSHIPS: Course -> Department ---
    """
    MATCH (c:Course), (d:Department {code: 'CSE'})
    WHERE c.code STARTS WITH 'CS'
    CREATE (c)-[:BELONGS_TO]->(d)
    """,
    """
    MATCH (c:Course {code: 'MATH101'}), (d:Department {code: 'CSE'})
    CREATE (c)-[:BELONGS_TO]->(d)
    """,

    # --- RELATIONSHIPS: Program -> Course (INCLUDES) ---
    """
    MATCH (p:Program {code: 'BTECH-CSE'}), (c:Course)
    WHERE c.code STARTS WITH 'CS' OR c.code = 'MATH101'
    CREATE (p)-[:INCLUDES]->(c)
    """,

    # --- RELATIONSHIPS: Course Prerequisites ---
    # Data Structures requires Intro to Programming
    """
    MATCH (a:Course {code: 'CS201'}), (b:Course {code: 'CS101'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # Algorithms requires Data Structures
    """
    MATCH (a:Course {code: 'CS301'}), (b:Course {code: 'CS201'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # DBMS requires Data Structures
    """
    MATCH (a:Course {code: 'CS302'}), (b:Course {code: 'CS201'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # OS requires Data Structures
    """
    MATCH (a:Course {code: 'CS303'}), (b:Course {code: 'CS201'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # Networks requires OS
    """
    MATCH (a:Course {code: 'CS401'}), (b:Course {code: 'CS303'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # AI requires Algorithms + Math
    """
    MATCH (a:Course {code: 'CS501'}), (b:Course {code: 'CS301'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    """
    MATCH (a:Course {code: 'CS501'}), (b:Course {code: 'MATH101'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # ML requires AI
    """
    MATCH (a:Course {code: 'CS502'}), (b:Course {code: 'CS501'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # Deep Learning requires ML
    """
    MATCH (a:Course {code: 'CS601'}), (b:Course {code: 'CS502'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # Cloud requires Networks
    """
    MATCH (a:Course {code: 'CS503'}), (b:Course {code: 'CS401'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,
    # Cybersecurity requires Networks
    """
    MATCH (a:Course {code: 'CS504'}), (b:Course {code: 'CS401'})
    CREATE (a)-[:HAS_PREREQUISITE]->(b)
    """,

    # --- RELATIONSHIPS: Faculty -> Course (TEACHES) ---
    """
    MATCH (f:Faculty {name: 'Dr. Mohammad Amjad'}), (c:Course {code: 'CS501'})
    CREATE (f)-[:TEACHES]->(c)
    """,
    """
    MATCH (f:Faculty {name: 'Dr. Mohammad Amjad'}), (c:Course {code: 'CS502'})
    CREATE (f)-[:TEACHES]->(c)
    """,
    """
    MATCH (f:Faculty {name: 'Dr. Tanvir Ahmad'}), (c:Course {code: 'CS601'})
    CREATE (f)-[:TEACHES]->(c)
    """,
    """
    MATCH (f:Faculty {name: 'Dr. Mohd Haroon'}), (c:Course {code: 'CS503'})
    CREATE (f)-[:TEACHES]->(c)
    """,
    """
    MATCH (f:Faculty {name: 'Dr. Raees Ahmad Khan'}), (c:Course {code: 'CS504'})
    CREATE (f)-[:TEACHES]->(c)
    """,
    """
    MATCH (f:Faculty {name: 'Dr. Khaleel Ahmad'}), (c:Course {code: 'CS302'})
    CREATE (f)-[:TEACHES]->(c)
    """,

    # --- RELATIONSHIPS: Faculty -> Department ---
    """
    MATCH (f:Faculty), (d:Department {code: 'CSE'})
    CREATE (f)-[:MEMBER_OF]->(d)
    """,
]


def run_seed():
    """Execute all Cypher seed statements."""
    print("=" * 60)
    print("IU NWEO AI — Neo4j Knowledge Graph Seed")
    print("=" * 60)

    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )

    with driver.session() as session:
        for i, cypher in enumerate(SEED_CYPHER):
            try:
                session.run(cypher.strip())
                print(f"  ✓ Statement {i + 1}/{len(SEED_CYPHER)} executed")
            except Exception as e:
                print(f"  ✗ Statement {i + 1} failed: {e}")

    # Verify
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY count DESC")
        print("\n--- Graph Summary ---")
        for record in result:
            print(f"  {record['label']}: {record['count']} nodes")

        rel_result = session.run("MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS count ORDER BY count DESC")
        print("\n--- Relationships ---")
        for record in rel_result:
            print(f"  {record['rel']}: {record['count']} edges")

    driver.close()
    print("\n✓ Neo4j seed complete.")
    print("=" * 60)


if __name__ == "__main__":
    run_seed()

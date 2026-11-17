
import sqlite3
from pathlib import Path
from datetime import datetime

# Database file location
DB_PATH = Path(__file__).parent / "resumeai.db"


# Connect to database
def connect_db():
    return sqlite3.connect(DB_PATH)


# Create database table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            job_description TEXT,
            similarity_score REAL,
            skill_match REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            analysis_date TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save resume analysis
def save_analysis(
    resume_name,
    job_description,
    similarity_score,
    skill_match,
    matched_skills,
    missing_skills
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resume_analysis (
            resume_name,
            job_description,
            similarity_score,
            skill_match,
            matched_skills,
            missing_skills,
            analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_name,
        job_description,
        similarity_score,
        skill_match,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# Get previous analysis records
def get_analysis_history():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM resume_analysis
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data

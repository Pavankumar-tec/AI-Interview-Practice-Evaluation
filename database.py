import json
import sqlite3
from datetime import datetime
from config import DATABASE_PATH

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Question Packs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_packs (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        version TEXT DEFAULT '1.0',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. Questions (supports both Descriptive and MCQ questions)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        pack_id TEXT NOT NULL,
        category TEXT NOT NULL,
        question_text TEXT NOT NULL,
        rubric_json TEXT NOT NULL,
        reference_material TEXT,
        difficulty TEXT DEFAULT 'Easy',
        keywords_json TEXT,
        question_type TEXT DEFAULT 'descriptive',
        options_json TEXT,
        correct_option TEXT,
        explanation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pack_id) REFERENCES question_packs (id)
    );
    """)
    
    # Auto-migration: ensure newly added columns exist if table was already created
    cursor.execute("PRAGMA table_info(questions);")
    columns = [col[1] for col in cursor.fetchall()]
    if "question_type" not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN question_type TEXT DEFAULT 'descriptive';")
    if "options_json" not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN options_json TEXT;")
    if "correct_option" not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN correct_option TEXT;")
    if "explanation" not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN explanation TEXT;")
    
    # 3. Interview Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_sessions (
        id TEXT PRIMARY KEY,
        candidate_name TEXT NOT NULL,
        category TEXT NOT NULL,
        pack_id TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 4. Candidate Answers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        question_id TEXT NOT NULL,
        answer_text TEXT NOT NULL,
        followup_question TEXT,
        followup_answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES interview_sessions (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    );
    """)
    
    # 5. Evaluations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        answer_id INTEGER NOT NULL,
        evaluation_method TEXT NOT NULL,
        overall_score REAL NOT NULL,
        criterion_scores_json TEXT NOT NULL,
        evidence_quotes_json TEXT NOT NULL,
        suggestions_json TEXT NOT NULL,
        followup_question TEXT,
        clarification_needed INTEGER DEFAULT 0,
        review_flag INTEGER DEFAULT 0,
        unsupported_feedback_count INTEGER DEFAULT 0,
        latency_ms INTEGER DEFAULT 0,
        token_cost REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (answer_id) REFERENCES candidate_answers (id)
    );
    """)
    
    # 6. Sample Answers (for 180 research answers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sample_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT UNIQUE NOT NULL,
        question_id TEXT NOT NULL,
        category TEXT NOT NULL,
        performance_level TEXT NOT NULL,
        source_type TEXT NOT NULL,
        answer_text TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    );
    """)
    
    # 7. Human Reviews (Reviewer 1 & Reviewer 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS human_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT NOT NULL,
        reviewer_id TEXT NOT NULL,
        overall_score REAL NOT NULL,
        criterion_scores_json TEXT NOT NULL,
        feedback_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sample_id) REFERENCES sample_answers (sample_id),
        UNIQUE(sample_id, reviewer_id)
    );
    """)
    
    # 8. Research Benchmark Evaluations (Method 1, 2, 3 over sample answers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT NOT NULL,
        method TEXT NOT NULL,
        overall_score REAL NOT NULL,
        criterion_scores_json TEXT NOT NULL,
        evidence_quotes_json TEXT NOT NULL,
        suggestions_json TEXT,
        unsupported_feedback_count INTEGER DEFAULT 0,
        latency_ms INTEGER DEFAULT 0,
        estimated_cost_usd REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sample_id) REFERENCES sample_answers (sample_id),
        UNIQUE(sample_id, method)
    );
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")

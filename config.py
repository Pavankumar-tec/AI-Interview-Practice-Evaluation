import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = BASE_DIR / "interview_practice.db"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mca-research-interview-secret-key-2026")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Research project metadata
    PROJECT_NAME = "AI Assisted Interview Practice and Evaluation"
    PROJECT_SUBTITLE = "Evidence Based Feedback and Adaptive Follow Up Questions"
    ACADEMIC_YEAR = "2026-2027"
    INSTITUTION = "Dr. Babasaheb Ambedkar Marathwada University"
    DEPARTMENT = "Department of Management Science, Chhatrapati Sambhajinagar"
    
    # LLM Settings
    DEFAULT_LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "offline_semantic") # 'offline_semantic', 'gemini', 'openai', 'anthropic'
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    
    # Target dataset sizes
    PILOT_QUESTIONS_COUNT = 45
    SAMPLE_ANSWERS_COUNT = 180

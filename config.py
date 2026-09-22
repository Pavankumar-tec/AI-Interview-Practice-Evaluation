import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get('DATABASE_PATH', str(BASE_DIR / 'interview_practice.db')))

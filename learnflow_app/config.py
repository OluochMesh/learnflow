import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Supabase PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:your_password@db.your-project-ref.supabase.co:5432/postgres'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # IntaSend Configuration
    INTASEND_PUBLIC_KEY = os.environ.get('INTASEND_PUBLIC_KEY')
    INTASEND_SECRET_KEY = os.environ.get('INTASEND_SECRET_KEY')
    INTASEND_WEBHOOK_SECRET = os.environ.get('INTASEND_WEBHOOK_SECRET')

# uweb_12/db_select.py

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_engine():
    # load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_12')
    
    # Detect environment
    is_heroku = os.getenv("HEROKU_ENV", "false").lower() == "true"
    is_render = os.getenv("RENDER_ENV", "false").lower() == "true"
    is_local = not is_heroku and not is_render

    if is_heroku:
        db_url = os.getenv('HEROKU_DB_URL')
        environment = "Heroku"
    elif is_render:
        db_url = os.getenv('RENDER_DB_URL') 
        # For Local Testing purposes
        # db_url = os.getenv('External_RENDER_DB_URL') 
        environment = "Render"
    else:
        db_url = os.getenv('LOCAL_DB_URL')
        environment = "Local"

    if not db_url:
        raise ValueError("No database URL found in environment variables.")
    
    db_url = db_url.replace('postgres://', 'postgresql+psycopg2://')

    # Create engine with connection pooling
    engine = create_engine(
        db_url,
        pool_size=10,           # Base pool size
        max_overflow=5,          # Max extra connections if pool is full
        pool_timeout=30,         # Timeout to get connection
        pool_recycle=1800,        # Recycle connections every 30 minutes
        pool_pre_ping=True  # ✅ Add this to auto-check if connection is alive
    )
    return engine, environment

engine, environment = get_database_engine()
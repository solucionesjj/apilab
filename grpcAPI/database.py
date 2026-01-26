import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LaMig2314")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "apilab")

# URL for connecting to MySQL Server (no specific DB) to check existence
SERVER_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
# URL for connecting to the specific Database
DATABASE_URL = f"{SERVER_URL}/{DB_NAME}"

def create_db_and_tables():
    # 1. Connect to MySQL server to create DB if it doesn't exist
    # We use a separate engine for this administrative task
    server_engine = create_engine(SERVER_URL)
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()  # Important for some drivers/configurations
    
    # 2. Connect to the actual database and create tables
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

# Create the engine globally (lazy initialization usually better but simple here)
# We will initialize it properly when the app starts or when needed
# For now, let's provide a factory or a global instance that gets set after creation
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_db_and_tables()
    return _engine

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

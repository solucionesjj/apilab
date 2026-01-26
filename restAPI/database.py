import os
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LaMig2314")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "apilab")

# URL base para conectar al servidor (sin base de datos específica)
DATABASE_SERVER_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
# URL completa para conectar a la base de datos
DATABASE_URL = f"{DATABASE_SERVER_URL}/{DB_NAME}"

# Engine global para la aplicación
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """
    Crea la base de datos si no existe y luego crea las tablas.
    """
    # 1. Conectar al servidor MySQL para crear la BD si no existe
    try:
        server_engine = create_engine(DATABASE_SERVER_URL)
        with server_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            print(f"Base de datos '{DB_NAME}' verificada/creada exitosamente.")
    except Exception as e:
        print(f"Error al intentar crear la base de datos: {e}")
        raise e

    # 2. Crear las tablas usando el engine que apunta a la BD
    try:
        # Importar modelos aquí para asegurar que SQLModel los registre antes de create_all
        from models import Producto
        SQLModel.metadata.create_all(engine)
        print("Tablas verificadas/creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        raise e

def get_session():
    with Session(engine) as session:
        yield session

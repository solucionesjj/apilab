import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Obtener credenciales de variables de entorno o usar valores por defecto
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LaMig2314") 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "apilab")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_if_not_exists():
    root_url = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/mysql"
    temp_engine = create_async_engine(root_url, isolation_level="AUTOCOMMIT", echo=True)
    try:
        async with temp_engine.connect() as conn:
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        await temp_engine.dispose()

async def init_db():
    await create_db_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

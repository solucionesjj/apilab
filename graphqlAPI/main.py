from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from datetime import datetime
from sqlmodel import select
from database import init_db, get_session
from models import Producto, ProductoCreate, ProductoUpdate
from schema import schema
import logging
import time
import sys

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Seed data from user requirements
SEED_PRODUCTS = [
    {
        "id": 1,
        "nombre": "Product one",
        "descripcion": "Description of product one",
        "precio": 22.22,
        "fecha_creacion": datetime.fromisoformat("2025-12-15T02:10:54"),
        "fecha_actualizacion": datetime.fromisoformat("2025-12-15T02:10:54")
    },
    {
        "id": 3,
        "nombre": "Producto 3",
        "descripcion": "Descripción del producto 3",
        "precio": 102.99,
        "fecha_creacion": datetime.fromisoformat("2025-12-15T02:14:58"),
        "fecha_actualizacion": datetime.fromisoformat("2025-12-15T02:14:58")
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB
    await init_db()
    
    # Check and seed data
    async for session in get_session():
        # Check products
        result = await session.exec(select(Producto))
        if not result.first():
            for p_data in SEED_PRODUCTS:
                product = Producto(**p_data)
                session.add(product)
            await session.commit()
    yield

app = FastAPI(lifespan=lifespan)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"Path: {request.url.path} Method: {request.method} Status: {response.status_code} Duration: {process_time:.2f}ms")
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(f"Path: {request.url.path} Method: {request.method} Duration: {process_time:.2f}ms Error: {str(e)}", exc_info=True)
        raise

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/api/v1/productos/")
async def get_products():
    async for session in get_session():
        result = await session.exec(select(Producto))
        return result.all()

@app.post("/api/v1/productos/", response_model=Producto)
async def create_product(producto: ProductoCreate):
    async for session in get_session():
        db_product = Producto.model_validate(producto)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

@app.put("/api/v1/productos/{id}", response_model=Producto)
async def update_product(id: int, producto: ProductoUpdate):
    async for session in get_session():
        db_product = await session.get(Producto, id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        product_data = producto.model_dump(exclude_unset=True)
        db_product.sqlmodel_update(product_data)
        db_product.fecha_actualizacion = datetime.now()
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

@app.delete("/api/v1/productos/{id}")
async def delete_product(id: int):
    async for session in get_session():
        db_product = await session.get(Producto, id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        await session.delete(db_product)
        await session.commit()
        return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    # Se obtiene el puerto de la variable de entorno PORT o se usa 8000 por defecto
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

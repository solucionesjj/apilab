import asyncio
import sys
import os
from contextlib import asynccontextmanager
from typing import List

# Ensure grpc_generated is in path for internal imports
sys.path.append(os.path.join(os.path.dirname(__file__), "grpc_generated"))

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from models import Producto
from grpc_server import serve_grpc

# REST Models (Pydantic) - we can reuse SQLModel or create specific ones
# For simplicity, using SQLModel directly

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    print("Base de datos inicializada.")
    
    # Start gRPC server in background
    # We create a task for it
    grpc_task = asyncio.create_task(serve_grpc())
    print("Tarea del servidor gRPC creada.")
    
    yield
    
    # Shutdown
    # In a real app we should gracefully stop the gRPC server
    grpc_task.cancel()
    try:
        await grpc_task
    except asyncio.CancelledError:
        print("Servidor gRPC detenido.")

app = FastAPI(
    title="API (FastAPI + gRPC)",
    description="API para mantener entidad Producto usando gRPC",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/products/", response_model=Producto)
def create_product(product: Producto, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products/", response_model=List[Producto])
def read_products(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    products = session.exec(select(Producto).offset(skip).limit(limit)).all()
    return products

@app.get("/products/{product_id}", response_model=Producto)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.put("/products/{product_id}", response_model=Producto)
def update_product(product_id: int, product_data: Producto, session: Session = Depends(get_session)):
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_dict = product_data.model_dump(exclude_unset=True)
    for key, value in product_dict.items():
        if key != "id": # Prevent ID update
            setattr(product, key, value)
            
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(product)
    session.commit()
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    # Run FastAPI on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8001)

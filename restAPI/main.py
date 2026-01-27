from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from database import init_db, get_session
from models import Producto, ProductoCreate, ProductoUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="API (FastAPI + REST)",
    description="API para mantener la entidad Producto usando REST",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/products/", response_model=Producto, status_code=201, summary="Crear un nuevo producto")
def create_producto(producto: ProductoCreate, session: Session = Depends(get_session)):
    db_producto = Producto.model_validate(producto)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@app.get("/products/", response_model=List[Producto], summary="Listar productos")
def read_productos(
    offset: int = 0, 
    limit: int = Query(default=100, le=100), 
    session: Session = Depends(get_session)
):
    """
    Obtiene una lista de productos con paginación opcional.
    """
    productos = session.exec(select(Producto).offset(offset).limit(limit)).all()
    return productos

@app.get("/products/{producto_id}", response_model=Producto, summary="Obtener un producto por ID")
def read_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Obtiene el detalle de un producto específico.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.patch("/products/{producto_id}", response_model=Producto, summary="Actualizar un producto")
def update_producto(producto_id: int, producto_update: ProductoUpdate, session: Session = Depends(get_session)):
    """
    Actualiza parcialmente un producto existente.
    """
    db_producto = session.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto_data = producto_update.model_dump(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    # Actualizar fecha de actualización
    db_producto.fecha_actualizacion = datetime.now()
    
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@app.delete("/products/{producto_id}", summary="Eliminar un producto")
def delete_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Elimina un producto de la base de datos.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    session.delete(producto)
    session.commit()
    return {"ok": True, "message": "Producto eliminado correctamente"}

if __name__ == "__main__":
    import uvicorn
    # Se obtiene el puerto de la variable de entorno PORT o se usa 8000 por defecto
    import os
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from datetime import datetime
from sqlmodel import select
from database import init_db, get_session
from models import Producto, Usuario, ProductoCreate, ProductoUpdate
from schema import schema

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

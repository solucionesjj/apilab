import strawberry
from typing import List, Optional
from sqlmodel import select
from datetime import datetime
from database import get_session
from models import Producto

# Define GraphQL Types
@strawberry.type
class ProductoType:
    id: int
    nombre: str
    descripcion: str
    precio: float
    fecha_creacion: datetime
    fecha_actualizacion: datetime

# Define Query
@strawberry.type
class Query:
    @strawberry.field
    async def productos(self) -> List[ProductoType]:
        try:
            async for session in get_session():
                statement = select(Producto)
                results = await session.exec(statement)
                return results.all()
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}", exc_info=True)
            raise Exception("Error interno al obtener productos") from e

# Define Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_producto(self, nombre: str, descripcion: str, precio: float) -> ProductoType:
        try:
            async for session in get_session():
                db_producto = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    fecha_creacion=datetime.now(),
                    fecha_actualizacion=datetime.now()
                )
                session.add(db_producto)
                await session.commit()
                await session.refresh(db_producto)
                return db_producto
        except Exception as e:
            logger.error(f"Error al crear producto: {e}", exc_info=True)
            raise Exception("Error interno al crear producto") from e

    @strawberry.mutation
    async def update_producto(self, id: int, nombre: Optional[str] = None, descripcion: Optional[str] = None, precio: Optional[float] = None) -> Optional[ProductoType]:
        try:
            async for session in get_session():
                statement = select(Producto).where(Producto.id == id)
                results = await session.exec(statement)
                db_producto = results.first()
                if not db_producto:
                    return None
                
                if nombre is not None:
                    db_producto.nombre = nombre
                if descripcion is not None:
                    db_producto.descripcion = descripcion
                if precio is not None:
                    db_producto.precio = precio
                
                db_producto.fecha_actualizacion = datetime.now()
                session.add(db_producto)
                await session.commit()
                await session.refresh(db_producto)
                return db_producto
        except Exception as e:
            logger.error(f"Error al actualizar producto {id}: {e}", exc_info=True)
            raise Exception(f"Error interno al actualizar producto {id}") from e

    @strawberry.mutation
    async def delete_producto(self, id: int) -> bool:
        try:
            async for session in get_session():
                statement = select(Producto).where(Producto.id == id)
                results = await session.exec(statement)
                db_producto = results.first()
                if not db_producto:
                    return False
                
                await session.delete(db_producto)
                await session.commit()
                return True
        except Exception as e:
            logger.error(f"Error al eliminar producto {id}: {e}", exc_info=True)
            raise Exception(f"Error interno al eliminar producto {id}") from e

schema = strawberry.Schema(query=Query, mutation=Mutation)

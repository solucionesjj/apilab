from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class ProductoBase(SQLModel):
    nombre: str
    descripcion: str
    precio: float

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None

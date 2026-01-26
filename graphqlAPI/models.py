from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: float
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)

class ProductoCreate(SQLModel):
    nombre: str
    descripcion: str
    precio: float

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: str
    nombre: str
    perfil: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)


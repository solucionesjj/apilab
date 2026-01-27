import grpc
from sqlmodel import Session, select
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grpc_generated"))

from grpc_generated import product_pb2, product_pb2_grpc
from database import get_engine
from models import Producto

class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.engine = get_engine()

    def _get_session(self):
        return Session(self.engine)

    def _model_to_response(self, product: Producto) -> product_pb2.ProductResponse:
        return product_pb2.ProductResponse(
            id=product.id,
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio=product.precio,
            fecha_creacion=product.fecha_creacion.isoformat() if product.fecha_creacion else "",
            fecha_actualizacion=product.fecha_actualizacion.isoformat() if product.fecha_actualizacion else ""
        )

    async def CreateProduct(self, request, context):
        with self._get_session() as session:
            new_product = Producto(
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio
            )
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            return self._model_to_response(new_product)

    async def GetProduct(self, request, context):
        with self._get_session() as session:
            product = session.get(Producto, request.id)
            if not product:
                context.abort(grpc.StatusCode.NOT_FOUND, "Producto no encontrado")
            return self._model_to_response(product)

    async def UpdateProduct(self, request, context):
        with self._get_session() as session:
            product = session.get(Producto, request.id)
            if not product:
                context.abort(grpc.StatusCode.NOT_FOUND, "Producto no encontrado")
            if request.nombre:
                product.nombre = request.nombre
            if request.descripcion:
                product.descripcion = request.descripcion
            if request.precio:
                product.precio = request.precio
            
            product.fecha_actualizacion = datetime.now()
            
            session.add(product)
            session.commit()
            session.refresh(product)
            return self._model_to_response(product)

    async def DeleteProduct(self, request, context):
        with self._get_session() as session:
            product = session.get(Producto, request.id)
            if not product:
                context.abort(grpc.StatusCode.NOT_FOUND, "Producto no encontrado") 
            
            session.delete(product)
            session.commit()
            return product_pb2.DeleteProductResponse(success=True)

    async def ListProducts(self, request, context):
        with self._get_session() as session:
            statement = select(Producto)
            results = session.exec(statement).all()
            return product_pb2.ListProductsResponse(
                products=[self._model_to_response(p) for p in results]
            )

async def serve_grpc():
    server = grpc.aio.server()
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"Servidor gRPC escuchando en {listen_addr}")
    await server.start()
    await server.wait_for_termination()

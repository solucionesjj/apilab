import asyncio
import grpc
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "grpc_generated"))

import product_pb2
import product_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = product_pb2_grpc.ProductServiceStub(channel)
        
        print("--- Crear Producto ---")
        response = await stub.CreateProduct(product_pb2.CreateProductRequest(
            nombre="Laptop Gamer",
            descripcion="High performance laptop",
            precio=1500.00
        ))
        print(f"Created: {response.id} - {response.nombre}")
        product_id = response.id
        
        print("\n--- Obtener Producto ---")
        response = await stub.GetProduct(product_pb2.GetProductRequest(id=product_id))
        print(f"Got: {response.nombre} - {response.precio}")
        
        print("\n--- Listar Productos ---")
        response = await stub.ListProducts(product_pb2.ListProductsRequest())
        for p in response.products:
            print(f"- {p.id}: {p.nombre}")

if __name__ == '__main__':
    asyncio.run(run())

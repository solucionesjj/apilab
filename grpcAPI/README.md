# API Lab, gRPC API

## Para regenerar archivo proto

```bash
python -m grpc_tools.protoc -I protos --python_out=grpc_generated --grpc_python_out=grpc_generated protos/product.proto
```
## Ejecución Todo

```bash
cd C:\Users\jmartinez\dev\apilab\grpcAPI
C:\Users\jmartinez\dev\apilab\grpcAPI\.venv\Scripts\activate.bat
python main.py

```

## Ejecución solo servidor

```bash
python grpc_server.py
```

## Ejecución cliente

```bash
python client_grpc.py
```
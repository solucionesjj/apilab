# API Producto (FastAPI + gRPC)

Este proyecto implementa una API para gestionar la entidad `Producto` utilizando **FastAPI** (REST + Swagger) y **gRPC**.

## Requisitos

- Python 3.10+
- MySQL Server en ejecución

## Instalación

1.  Crear entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

La aplicación utiliza variables de entorno para conectar a la base de datos. Crea un archivo `.env` en la raíz (opcional, ya que hay valores por defecto) con el siguiente contenido si necesitas cambiar algo:

```env
DB_USER=root
DB_PASSWORD=LaMig2314
DB_HOST=localhost
DB_PORT=3306
DB_NAME=apilab
```

> **Nota:** La aplicación intentará crear la base de datos `apilab` si no existe al iniciar.

## Generación de Código gRPC (si modificas .proto)

Si modificas el archivo `protos/product.proto`, regenera el código Python:

```bash
python -m grpc_tools.protoc -I protos --python_out=grpc_generated --grpc_python_out=grpc_generated protos/product.proto
```

## Ejecución

Para iniciar tanto el servidor FastAPI como el servidor gRPC (que se ejecuta en segundo plano):

```bash
python main.py
```

- **FastAPI (REST + Swagger):** http://localhost:8000/docs
- **gRPC Server:** localhost:50051

## Pruebas

### Probar gRPC
Ejecuta el cliente de prueba incluido:

```bash
python client_grpc.py
```

### Probar REST
Abre http://localhost:8000/docs en tu navegador y utiliza la interfaz de Swagger UI.

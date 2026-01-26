# Ejemplos de prueba con cURL

Asegúrate de que tu servidor esté corriendo antes de ejecutar estos comandos:
```bash
python main.py
```

## 1. Crear un Producto (POST)
```bash
curl -X POST "http://localhost:8000/products/" \
     -H "Content-Type: application/json" \
     -d "{\"nombre\": \"Mouse Ergonómico\", \"descripcion\": \"Mouse vertical inalámbrico\", \"precio\": 45.50}"
```

## 2. Listar Productos (GET)
```bash
curl -X GET "http://localhost:8000/products/"
```

## 3. Obtener un Producto por ID (GET)
Reemplaza `1` con el ID del producto que quieras consultar.
```bash
curl -X GET "http://localhost:8000/products/1"
```

## 4. Actualizar un Producto (PUT)
Reemplaza `1` con el ID del producto a actualizar.
```bash
curl -X PUT "http://localhost:8000/products/1" \
     -H "Content-Type: application/json" \
     -d "{\"nombre\": \"Mouse Pro\", \"precio\": 50.00}"
```

## 5. Eliminar un Producto (DELETE)
Reemplaza `1` con el ID del producto a eliminar.
```bash
curl -X DELETE "http://localhost:8000/products/1"
```

---

## Nota para PowerShell (Windows)
Si estás usando PowerShell, `curl` es un alias de `Invoke-WebRequest`. Para usar el `curl` real, usa `curl.exe` o el comando completo así:

**Crear (PowerShell):**
```powershell
curl.exe -X POST "http://localhost:8000/products/" `
     -H "Content-Type: application/json" `
     -d '{"nombre": "Teclado Mecánico", "descripcion": "RGB Switch Blue", "precio": 89.99}'
```

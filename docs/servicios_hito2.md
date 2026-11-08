# Catálogo de servicios — endpoints implementados (Gastón)

| HTTP | Ruta | Permiso | Comportamiento |
|---|---|---|---|
| GET | /api/servicios | cliente/admin | Lista servicios activos |
| GET | /api/servicios/{id} | cliente/admin | Obtiene un servicio activo |
| POST | /api/servicios | admin | Crea servicio; JSON `nombre`, `precio` |
| PUT | /api/servicios/{id} | admin | Actualiza ambos campos |
| DELETE | /api/servicios/{id} | admin | Baja lógica (`activo=0`) |

Precios expresados como enteros positivos, de acuerdo con el modelo del grupo.
Autenticación con sesión Flask (`session['id_usuario']`) o HTTP Basic **solo sobre HTTPS/localhost**.
Los roles se comprueban con los datos reales de la base. El frontend debe comunicarse
con el backend mediante la biblioteca Python `requests`.

Crear las tablas con `bd/servicios.sql` en la base `cine_paradiso`.
La baja lógica conserva referencias de consumos históricos.

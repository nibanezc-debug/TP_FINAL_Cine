# Entradas — endpoints implementados — (Santiago)

| HTTP | Ruta | Permiso | Comportamiento |
|---|---|---|---|
| POST | /api/entradas | cliente | Compra: JSON `id_funcion`, `butacas` (lista de ids). Crea la reserva en `pendiente` y una entrada con QR por butaca; 409 si alguna butaca ya está vendida |
| GET | /api/entradas | admin | Lista todas las entradas; filtros `id_funcion`, `id_usuario`, `estado` |
| GET | /api/entradas/mias | usuario logueado | Lista las entradas propias; filtro `estado` |
| GET | /api/entradas/{id} | dueño/admin | Detalle de una entrada (incluye `codigo_qr`) |
| GET | /api/entradas/{id}/qr | dueño/admin | Imagen PNG del QR; solo entradas activas |
| GET | /api/entradas/{id}/factura | dueño/admin | Entradas y servicios de la reserva con totales (las canceladas no suman) |
| POST | /api/entradas/{id}/reenviar | dueño/admin | Envía la entrada con el QR por mail al dueño; 503 si el SMTP no está configurado |
| PATCH | /api/entradas/{id}/cancelar | dueño/admin | Cancela una entrada activa y libera la butaca; 422 fuera de plazo, 409 si ya fue usada o cancelada |
| POST | /api/entradas/validar | admin | JSON `codigo_qr`, `id_funcion`; verifica función y fecha y la marca como `usada`; 404, 409 o 422 si no es válida |
| GET | /api/entradas/estadisticas/cancelaciones | admin | Cancelaciones y porcentaje; parámetros `agrupar` (`funcion` o `pelicula`), `desde`, `hasta` |
| GET | /api/entradas/estadisticas/franjas-horarias | admin | Entradas vendidas y recaudado por hora, de mayor a menor; parámetros `desde`, `hasta` |

Una butaca no puede venderse dos veces en la misma función: lo garantiza una restricción `UNIQUE (id_funcion, butaca_activa)` en la base y una transacción en la compra. Al cancelar, la butaca queda libre y la entrada se conserva para las estadísticas. La cancelación se permite hasta 120 minutos antes de la función (`MINUTOS_LIMITE_CANCELACION` en `services/entradas.py`). Las fechas se guardan en un único campo `DATETIME`. Los precios son enteros positivos, igual que en servicios.

Autenticación con sesión Flask (`session['id_usuario']`) o HTTP Basic **solo sobre HTTPS/localhost**. Los roles se comprueban con los datos reales de la base. El frontend debe comunicarse con el backend mediante la biblioteca Python `requests`.

Crear la tabla con `bd/entradas.sql` en la base `cine_paradiso`, después de `reservas`, `funciones` y `butacas`. El QR requiere `qrcode[pil]` en `requirements.txt`. El reenvío por mail usa las variables `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` y `SMTP_FROM`.

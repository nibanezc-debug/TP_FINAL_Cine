# Consumos de reservas — endpoints implementados (Günter)

| HTTP | Ruta | Permiso | Comportamiento |
|---|---|---|---|
| GET | /api/reservas/{id}/consumos | titular/admin | Lista servicios de una reserva |
| POST | /api/reservas/{id}/consumos | titular | Agrega `{ "id_servicio": 1, "cantidad": 2 }` |
| DELETE | /api/reservas/{id}/consumos/{id_consumo} | titular | Quita consumo si la reserva está pendiente |

**Contrato con el módulo de entradas:** se espera la tabla `reservas` con columnas
`id`, `id_usuario` y `estado`. Para modificar, `estado` debe ser `pendiente`.
Hay que consensuar esas columnas y el momento de confirmación de la compra con
el compañero responsable de entradas. El precio de cada consumo se toma de la
base y se guarda al crear la línea para preservar el valor histórico.

La tabla `consumos` se crea ejecutando `bd/consumos.sql` luego de crear
`reservas` y `servicios`. Solo las rutas autenticadas pueden operar consumos.

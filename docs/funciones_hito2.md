# Funciones — POST, PATCH y DELETE (Ignacio)

Se mantienen intactos los GET implementados para `/api/cartelera`, `/api/funciones` y `/api/funciones/{id}`.

| Método | Ruta | Permiso | Resultado |
|---|---|---|---|
| POST | `/api/funciones` | administrador | 201 y `{"id": 12}` |
| PATCH | `/api/funciones/{id}` | administrador | 204, edición parcial |
| DELETE | `/api/funciones/{id}` | administrador | 204, eliminación física si es seguro |

## Ejemplos

**POST** `/api/funciones`

```json
{
  "id_pelicula": 1,
  "id_sala": 2,
  "fecha_hora": "2035-11-10 20:00:00",
  "precio": 5000
}
```

**PATCH** `/api/funciones/12` (se puede enviar cualquier combinación no vacía de esos cuatro campos)

```json
{ "precio": 6500 }
```

**DELETE** `/api/funciones/12`: no requiere cuerpo.

## Validaciones y restricciones adoptadas

- Los tres endpoints requieren rol `administrador`.
- El POST requiere `id_pelicula`, `id_sala`, `fecha_hora` y `precio`; PATCH admite solo los campos que cambian.
- IDs y precio: enteros positivos (sin aceptar booleanos); la fecha debe incluir hora y segundos.
- Deben existir la película y la sala. La película debe estar activa, tener duración positiva y estar disponible en la fecha elegida.
- Una sala no puede tener funciones superpuestas (se utiliza la duración de cada película).
- No se pueden crear o modificar funciones para fechas pasadas.
- Una función con entradas emitidas **no se puede modificar ni eliminar**, aunque las entradas estén canceladas, para preservar el historial.
- Las funciones pasadas no se pueden eliminar; se utiliza DELETE físico solo para funciones futuras sin entradas.
- Respuestas: 400 (datos inválidos), 401 (sin login), 403 (sin permiso), 404 (recurso inexistente), 409 (conflicto), 201/204 (éxito).

**Importante:** estas reglas de PATCH/DELETE son una propuesta conservadora. Si el equipo acordó otras reglas (por ejemplo permitir cambios de precio con entradas emitidas), deben revisarse juntos.

El archivo `bd/funciones.sql` corrige la FK `id_pelicula` para referenciar `peliculas(id_pelicula)` tal como figura en `bd/peliculas.sql`. Si la tabla `funciones` ya está creada, este cambio del script no migra la base existente.

### Pruebas

```bash
python -m unittest tests/test_funciones.py tests/test_rutas_funciones.py
```

Se necesita instalar `requirements.txt`, configurar `FLASK_SECRET_KEY` y tener el esquema de base compatible. Las pruebas mockean el repositorio; no reemplazan una prueba de integración contra MySQL con dos funciones superpuestas y entradas vendidas.

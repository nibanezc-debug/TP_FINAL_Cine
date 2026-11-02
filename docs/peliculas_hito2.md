# Películas — endpoints implementados (Fernando)

| HTTP | Ruta | Permiso | Comportamiento |
| :--- | :--- | :--- | :--- |
| GET | `/api/peliculas/externas` | admin | Búsqueda externa en OMDB; parámetro `titulo`. Devuelve hasta 5 resultados con detalle completo; 502 si OMDB rechaza por límite o clave |
| GET | `/api/peliculas` | usuario logueado | Lista películas; filtros `titulo`, `genero`, `activa`. Los clientes tienen forzado el filtro `activa = True` |
| GET | `/api/peliculas/{id}` | usuario logueado | Detalle de una película. 404 si no existe o si es un cliente consultando una película inactiva |
| POST | `/api/peliculas` | admin | Crea película: JSON `titulo`, `sinopsis`, `poster_url`, `duracion_minutos`, fechas, etc. Retorna `id_pelicula` |
| PUT | `/api/peliculas/{id}` | admin | Actualiza los datos completos de una película existente; 404 si no existe, 400 por validación de tipos o fechas |
| DELETE | `/api/peliculas/{id}` | admin | Baja lógica: marca la película con `activa = False` conservando el historial; 404 si no existe |

La baja de películas se maneja de forma lógica (campo `activa` tipo `BOOLEAN` en la base) para no romper las relaciones con las funciones y entradas históricas. La validación de fechas asegura que `disponible_desde` nunca sea posterior a `disponible_hasta` y se almacenan en un único campo `DATETIME` como exige el enunciado. El consumo a OMDB se aísla en `services/peliculas.py`, manejando timeouts, excepciones de red y distinguiendo el error `Movie not found!` (devuelve array vacío) de caídas reales de la API (levanta 502). 

Autenticación con sesión Flask (`session['id_usuario']`) o HTTP Basic **solo sobre HTTPS/localhost**. Los roles se comprueban con los datos reales de la base a través de los decoradores `@requiere_admin` y `@requiere_usuario`. El frontend debe comunicarse con el backend mediante la biblioteca Python `requests`.

Crear la tabla con `bd/peliculas.sql` en la base `cine_paradiso`. Al ser una entidad principal, puede crearse antes que `funciones` y `salas`. Las peticiones externas requieren `requests` y `python-dotenv` en `requirements.txt`. El funcionamiento de la búsqueda externa depende de la variable `OMDB_API_KEY` en el entorno; si no está configurada, el servidor lanzará error 500 para evitar fugas y fallos silenciosos.

# Documentación de Endpoints — Módulo de Películas

**Especificaciones Generales**

* **Formato de datos:** Todos los datos enviados y recibidos se procesan en formato JSON.
* **Seguridad y Roles:** El sistema distingue entre rol `cliente` y `administrador`. Se valida mediante los decoradores `@requiere_usuario` y `@requiere_admin`.
* **Prefijo de rutas:** Todas las rutas asumen el prefijo `/api` registrado en `app.py`.

---

### 1. Buscar Películas Externas (OMDB)

* **Ruta:** `/api/peliculas/externas?titulo={busqueda}`
* **Método HTTP:** `GET`
* **Permisos:** Administrador
* **Descripción:** Consume la API externa de OMDB para buscar películas por título y devuelve un listado de hasta 5 coincidencias detalladas, formateadas para ser insertadas directamente en la base local.

* **Respuesta satisfactoria (Código 200 OK):**
```json
{
    "resultados": [
        {
            "imdb_id": "tt3896198",
            "titulo": "Guardians of the Galaxy Vol. 2",
            "sinopsis": "The Guardians struggle to keep together as a team...",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNWE5...",
            "duracion_minutos": 136,
            "clasificacion": "PG-13",
            "genero": "Action, Adventure, Comedy"
        }
    ]
}
```

* **Respuesta de error (Código 502 Bad Gateway):**
```json
{
    "error": "OMDB rechazó la petición: Request limit reached!"
}
```

---

### 2. Listar Películas (Cartelera y Backoffice)

* **Ruta:** `/api/peliculas`
* **Método HTTP:** `GET`
* **Permisos:** Cliente / Administrador
* **Descripción:** Devuelve la lista de películas. Permite filtros por query params (`?titulo=`, `?genero=`, `?activa=`). Los usuarios con rol `cliente` solo recibirán películas con `activa = True`, independientemente del filtro enviado.

* **Respuesta satisfactoria (Código 200 OK):**
```json
{
    "peliculas": [
        {
            "id_pelicula": 1,
            "titulo": "Dune: Part Two",
            "sinopsis": "Paul Atreides unites with Chani...",
            "poster_url": "https://link-al-poster.com/dune2.jpg",
            "duracion_minutos": 166,
            "clasificacion": "PG-13",
            "genero": "Sci-Fi, Adventure",
            "disponible_desde": "2026-10-01 00:00:00",
            "disponible_hasta": "2026-12-31 23:59:59",
            "activa": true
        }
    ]
}
```

---

### 3. Obtener Detalle de Película

* **Ruta:** `/api/peliculas/<int:id>`
* **Método HTTP:** `GET`
* **Permisos:** Cliente / Administrador
* **Descripción:** Obtiene todos los datos de una película específica. Si la película tiene `activa = False`, retornará un 404 para los clientes.

* **Respuesta satisfactoria (Código 200 OK):**
```json
{
    "id_pelicula": 1,
    "titulo": "Dune: Part Two",
    "sinopsis": "Paul Atreides unites with Chani...",
    "poster_url": "https://link-al-poster.com/dune2.jpg",
    "duracion_minutos": 166,
    "clasificacion": "PG-13",
    "genero": "Sci-Fi, Adventure",
    "disponible_desde": "2026-10-01 00:00:00",
    "disponible_hasta": "2026-12-31 23:59:59",
    "activa": true
}
```

* **Respuesta de error (Código 404 Not Found):**
```json
{
    "error": "No se encontró la película con ID 1"
}
```

---

### 4. Crear Película

* **Ruta:** `/api/peliculas`
* **Método HTTP:** `POST`
* **Permisos:** Administrador
* **Descripción:** Carga una nueva película en la cartelera local. Los datos pueden provenir de la búsqueda externa de OMDB o cargarse manualmente.

* **Cuerpo de la Petición (Request JSON):**
```json
{
    "titulo": "The Matrix",
    "sinopsis": "Un hacker descubre la verdadera naturaleza de su realidad.",
    "poster_url": "https://link-al-poster.com/matrix.jpg",
    "duracion_minutos": 136,
    "clasificacion": "R",
    "genero": "Action, Sci-Fi",
    "disponible_desde": "2026-11-01 10:00:00",
    "disponible_hasta": "2026-11-30 23:59:59"
}
```

* **Respuesta satisfactoria (Código 201 Created):**
```json
{
    "id_pelicula": 2
}
```

* **Respuesta de error (Código 400 Bad Request):**
```json
{
    "error": "La duración en minutos debe ser un entero positivo válido"
}
```

---

### 5. Actualizar Película

* **Ruta:** `/api/peliculas/<int:id>`
* **Método HTTP:** `PUT`
* **Permisos:** Administrador
* **Descripción:** Reemplaza los datos de una película existente.

* **Cuerpo de la Petición (Request JSON):**
*(Mismo formato que el POST)*

* **Respuesta satisfactoria (Código 204 No Content):**
*(El servidor responde sin cuerpo, indicando que la operación fue exitosa)*

* **Respuesta de error (Código 404 Not Found):**
```json
{
    "error": "No se encontró la película con ID 2"
}
```

---

### 6. Eliminar Película (Baja Lógica)

* **Ruta:** `/api/peliculas/<int:id>`
* **Método HTTP:** `DELETE`
* **Permisos:** Administrador
* **Descripción:** Da de baja una película ocultándola de la cartelera (`activa = False`), pero preservándola en la base de datos para no afectar el historial de entradas y funciones.

* **Respuesta satisfactoria (Código 204 No Content):**
*(El servidor responde sin cuerpo, indicando que la operación fue exitosa)*

* **Respuesta de error (Código 404 Not Found):**
```json
{
    "error": "No se encontró la película con ID 2"
}
```
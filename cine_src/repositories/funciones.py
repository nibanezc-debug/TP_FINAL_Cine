from mysql.connector import IntegrityError

from db import consultar_todos, consultar_uno, ejecutar
from errors import ApiError


def buscar_funcion_por_id(id_funcion):
    query = """
        SELECT
            f.id, f.id_pelicula, f.id_sala, f.fecha_hora, f.precio,
            p.titulo, p.sinopsis, p.poster_url, p.duracion_minutos, p.clasificacion,
            s.nombre AS sala, s.id_local, l.nombre AS local
        FROM funciones f
        JOIN peliculas p ON p.id_pelicula = f.id_pelicula
        JOIN salas s ON s.id = f.id_sala
        JOIN locales l ON l.id = s.id_local
        WHERE f.id = %s
    """

    return consultar_uno(query, (id_funcion,))


def listar_funciones(
    id_pelicula=None, id_local=None, id_sala=None, fecha=None, en_cartelera=False
):
    query = """
        SELECT
            f.id, f.id_pelicula, f.id_sala, f.fecha_hora, f.precio,
            p.titulo, p.sinopsis, p.poster_url, p.duracion_minutos, p.clasificacion,
            s.nombre AS sala, s.id_local, l.nombre AS local
        FROM funciones f
        JOIN peliculas p ON p.id_pelicula = f.id_pelicula
        JOIN salas s ON s.id = f.id_sala
        JOIN locales l ON l.id = s.id_local
        WHERE 1 = 1
    """

    params = []

    if id_pelicula is not None:
        query += " AND f.id_pelicula = %s"
        params.append(id_pelicula)

    if id_local is not None:
        query += " AND s.id_local = %s"
        params.append(id_local)

    if id_sala is not None:
        query += " AND f.id_sala = %s"
        params.append(id_sala)

    if fecha is not None:
        query += " AND DATE(f.fecha_hora) = %s"
        params.append(fecha)

    if en_cartelera:
        query += " AND f.fecha_hora > NOW()"
        query += " AND p.activa = TRUE"
        query += """
            AND (
                p.disponible_desde IS NULL
                OR f.fecha_hora >= p.disponible_desde
            )
            AND (
                p.disponible_hasta IS NULL
                OR f.fecha_hora <= p.disponible_hasta
            )
        """

    query += " ORDER BY f.fecha_hora, f.id"

    return consultar_todos(query, tuple(params))


def listar_cartelera(id_local=None, fecha=None):
    return listar_funciones(
        id_local=id_local,
        fecha=fecha,
        en_cartelera=True,
    )


# Consultas de apoyo para las reglas de negocio del CRUD.
def buscar_pelicula(id_pelicula):
    sql = """SELECT id_pelicula, activa, duracion_minutos,
                    disponible_desde, disponible_hasta
             FROM peliculas WHERE id_pelicula = %s"""
    return consultar_uno(sql, (id_pelicula,))


def buscar_sala(id_sala):
    return consultar_uno("SELECT id FROM salas WHERE id = %s", (id_sala,))


def tiene_entradas(id_funcion):
    # Incluye entradas canceladas para conservar el historial.
    return consultar_uno("SELECT id FROM entradas WHERE id_funcion = %s LIMIT 1", (id_funcion,)) is not None


def hay_superposicion(id_sala, inicio, fin, id_funcion=None):
    # Se calcula el final de las funciones usando la duración de su película.
    sql = """
        SELECT f.id FROM funciones f
        JOIN peliculas p ON p.id_pelicula = f.id_pelicula
        WHERE f.id_sala = %s
          AND f.fecha_hora < %s
          AND DATE_ADD(
              f.fecha_hora,
              INTERVAL GREATEST(COALESCE(p.duracion_minutos, 0), 1) MINUTE
          ) > %s
    """
    parametros = [id_sala, fin, inicio]
    if id_funcion is not None:
        sql += " AND f.id <> %s"
        parametros.append(id_funcion)
    return consultar_uno(sql + " LIMIT 1", tuple(parametros)) is not None


def crear_funcion(datos):
    sql = """INSERT INTO funciones (id_pelicula, id_sala, fecha_hora, precio)
             VALUES (%s, %s, %s, %s)"""
    parametros = (datos["id_pelicula"], datos["id_sala"], datos["fecha_hora"], datos["precio"])
    try:
        id_nuevo, _ = ejecutar(sql, parametros)
    except IntegrityError as error:
        if error.errno == 1062:
            raise ApiError("Ya existe una función en esa sala y horario", 409) from error
        raise
    return id_nuevo


def modificar_funcion(id_funcion, datos):
    # Las columnas vienen del validador, no del usuario directamente.
    cambios = [f"{campo} = %s" for campo in datos]
    parametros = tuple(datos.values()) + (id_funcion,)
    sql = f"UPDATE funciones SET {', '.join(cambios)} WHERE id = %s"
    try:
        _, filas = ejecutar(sql, parametros)
    except IntegrityError as error:
        if error.errno == 1062:
            raise ApiError("Ya existe una función en esa sala y horario", 409) from error
        raise
    return filas > 0


def eliminar_funcion(id_funcion):
    _, filas = ejecutar("DELETE FROM funciones WHERE id = %s", (id_funcion,))
    return filas > 0

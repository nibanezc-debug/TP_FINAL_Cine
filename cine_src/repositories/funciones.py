from db import consultar_todos, consultar_uno


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

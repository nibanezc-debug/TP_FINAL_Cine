from db import consultar_todos, consultar_uno, ejecutar, ejecutar_muchos

CAPACIDADES_PERMITIDAS = {
    120: (10, 12),
    250: (10, 25),
    450: (15, 30),
}


def listar_salas_por_local(id_local, formato=None, capacidad=None, limit=10, offset=0):
    query = "SELECT * FROM salas WHERE id_local = %s"
    params = [id_local]

    if formato:
        query += " AND formato = %s"
        params.append(formato)

    if capacidad is not None:
        query += " AND capacidad >= %s"
        params.append(capacidad)

    query += " LIMIT %s OFFSET %s"
    params.extend([int(limit), int(offset)])

    return consultar_todos(query, tuple(params))


def contar_total_salas(id_local, formato=None, capacidad=None):
    query = "SELECT COUNT(*) AS total FROM salas WHERE id_local = %s"
    params = [id_local]

    if formato:
        query += " AND formato = %s"
        params.append(formato)

    if capacidad is not None:
        query += " AND capacidad >= %s"
        params.append(capacidad)

    resultado = consultar_uno(query, tuple(params))
    return resultado['total'] if resultado else 0


def buscar_local_por_id(id_local):
    return consultar_uno("SELECT * FROM locales WHERE id = %s", (id_local,))


def obtener_dimensiones_sala(capacidad):
    if capacidad not in CAPACIDADES_PERMITIDAS:
        raise ValueError(
            f"Capacidad '{capacidad}' no válida. Las capacidades permitidas son: 120, 250 o 450."
        )
    return CAPACIDADES_PERMITIDAS[capacidad]


def buscar_sala_por_id(id_sala):
    return consultar_uno("SELECT * FROM salas WHERE id = %s", (id_sala,))


def buscar_sala_en_funciones(id_sala):
    return consultar_uno("SELECT * FROM funciones WHERE id_sala = %s", (id_sala,))
from db import consultar_todos, consultar_uno, ejecutar


def listar_salas_por_local(id_local, formato=None, capacidad=None, limit=10, offset=0):
    query = "SELECT * FROM salas WHERE id_local = %s"
    params = [id_local]

    if formato:
        query += " AND formato = %s"
        params.append(formato)

    if capacidad is not None:
        query += " AND capacidad >= %s"
        params.append(capacidad)

    query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
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


def agregar_sala(data, id_local):
    sql = "INSERT INTO salas (nombre, capacidad, formato, id_local) VALUES (%s, %s, %s, %s)"
    params = (data.get('nombre'), data.get('capacidad'), data.get('formato'), id_local)
    id_creado, _ = ejecutar(sql, params)
    return id_creado


def actualizar_sala(data, id_sala):
    campos = []
    params = []

    if 'nombre' in data and data['nombre'] is not None:
        campos.append("nombre = %s")
        params.append(data['nombre'])

    if 'capacidad' in data and data['capacidad'] is not None:
        campos.append("capacidad = %s")
        params.append(data['capacidad'])

    if 'formato' in data and data['formato'] is not None:
        campos.append("formato = %s")
        params.append(data['formato'])

    if not campos:
        return 0

    params.append(id_sala)
    sql = f"UPDATE salas SET {', '.join(campos)} WHERE id = %s"
    _, filas_afectadas = ejecutar(sql, tuple(params))
    return filas_afectadas


def buscar_sala_por_id(id_sala):
    return consultar_uno("SELECT * FROM salas WHERE id = %s", (id_sala,))


def eliminar_sala(id_sala):
    _, filas_afectadas = ejecutar("DELETE FROM salas WHERE id = %s", (id_sala,))
    return filas_afectadas


def buscar_sala_en_funciones(id_sala):
    return consultar_uno("SELECT * FROM funciones WHERE id_sala = %s", (id_sala,))
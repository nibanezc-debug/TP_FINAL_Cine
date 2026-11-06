from db import obtener_conexion as conexion

def listar_salas_por_local(id_local, formato=None, capacidad=None, limit=10, offset=0):
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT * FROM salas WHERE id_local = %s"
    params = [id_local]

    if formato:
        query += " AND formato = %s"
        params.append(formato)

    if capacidad is not None:
        query += " AND capacidad >= %s"
        params.append(capacidad)

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, params)
    return cursor.fetchall()


def contar_total_salas(id_local, formato=None, capacidad=None):
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT COUNT(*) AS total FROM salas WHERE id_local = %s"
    params = [id_local]

    if formato:
        query += " AND formato = %s"
        params.append(formato)

    if capacidad is not None:
        query += " AND capacidad >= %s"
        params.append(capacidad)

    cursor.execute(query, params)
    resultado = cursor.fetchone()
    return resultado['total'] if resultado else 0


def buscar_local_por_id(id_local):
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT * FROM locales WHERE id_local = %s"
    params = (id_local,)
    cursor.execute(query, params)
    return cursor.fetchone()


def agregar_sala(data, id_local):
    cursor = conexion.cursor(dictionary=True)

    nombre = data.get('nombre')
    capacidad = data.get('capacidad')
    formato = data.get('formato')

    query = "INSERT INTO salas (nombre, capacidad, formato, id_local) VALUES (%s, %s, %s, %s)"
    params = (nombre, capacidad, formato, id_local)
    cursor.execute(query, params)
    conexion.commit()


def actualizar_sala(data, id_sala):
    cursor = conexion.cursor(dictionary=True)

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
        return

    query = f"UPDATE salas SET {', '.join(campos)} WHERE id_sala = %s"
    params.append(id_sala)

    cursor.execute(query, params)
    conexion.commit()


def buscar_sala_por_id(id_sala):
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT * FROM salas WHERE id_sala = %s"
    params = (id_sala,)
    cursor.execute(query, params)
    return cursor.fetchone()


def eliminar_sala(id_sala):
    cursor = conexion.cursor(dictionary=True)

    query = "DELETE FROM salas WHERE id_sala = %s"
    params = (id_sala,)
    cursor.execute(query, params)
    conexion.commit()


def buscar_sala_en_funciones(id_sala):
    cursor = conexion.cursor(dictionary=True)

    query = "SELECT * FROM funciones WHERE id_sala = %s"
    params = (id_sala,)
    cursor.execute(query, params)
    return cursor.fetchone()
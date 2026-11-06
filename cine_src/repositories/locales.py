from db import obtener_conexion as conexion


def listar_locales():
    query = "SELECT * FROM locales"
    
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def agregar_local(data):
    nombre = data.get('nombre')
    direccion = data.get('direccion')

    query = "INSERT INTO locales (nombre, direccion) VALUES (%s, %s)"
    params = (nombre, direccion)

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        conexion.commit()


def buscar_local_por_id(id_local):
    query = "SELECT * FROM locales WHERE id_local = %s"
    params = (id_local,)

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def actualizar_local(data, id_local):
    campos = []
    params = []

    if 'nombre' in data and data['nombre'] is not None:
        campos.append("nombre = %s")
        params.append(data['nombre'])

    if 'direccion' in data and data['direccion'] is not None:
        campos.append("direccion = %s")
        params.append(data['direccion'])

    if not campos:
        return

    query = f"UPDATE locales SET {', '.join(campos)} WHERE id_local = %s"
    params.append(id_local)

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        conexion.commit()


def eliminar_local(id_local):
    query = "DELETE FROM locales WHERE id_local = %s"
    params = (id_local,)

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        conexion.commit()


def contar_salas_de_local(id_local):
    query = "SELECT COUNT(*) AS total FROM salas WHERE id_local = %s"
    params = (id_local,)

    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        resultado = cursor.fetchone()
        return resultado['total'] if resultado else 0
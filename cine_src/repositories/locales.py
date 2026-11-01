from cine_src.db import obtener_conexion as conexion

def listar_locales():
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM locales"
    cursor.execute(query)
    locales = cursor.fetchall()
    cursor.close()
    return locales


def agregar_local(data):
    cursor = conexion.cursor(dictionary=True)
    nombre = data.get('nombre')
    direccion = data.get('direccion')

    query = "INSERT INTO locales (nombre, direccion) VALUES (%s, %s)"
    params = (nombre, direccion)
    
    cursor.execute(query, params)
    conexion.commit()
    cursor.close()


def buscar_local_por_id(id_local):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM locales WHERE id_local = %s"
    params = (id_local,)
    
    cursor.execute(query, params)
    local = cursor.fetchone()
    cursor.close()
    return local


def actualizar_local(data, id_local):
    cursor = conexion.cursor(dictionary=True)

    campos = []
    params = []

    if 'nombre' in data and data['nombre'] is not None:
        campos.append("nombre = %s")
        params.append(data['nombre'])

    if 'direccion' in data and data['direccion'] is not None:
        campos.append("direccion = %s")
        params.append(data['direccion'])

    if not campos:
        cursor.close()
        return

    query = f"UPDATE locales SET {', '.join(campos)} WHERE id_local = %s"
    params.append(id_local)

    cursor.execute(query, tuple(params))
    conexion.commit()
    cursor.close()


def eliminar_local(id_local):
    cursor = conexion.cursor(dictionary=True)
    query = "DELETE FROM locales WHERE id_local = %s"
    params = (id_local,)
    
    cursor.execute(query, params)
    conexion.commit()
    cursor.close()


def contar_salas_de_local(id_local):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT COUNT(*) AS total FROM salas WHERE id_local = %s"
    params = (id_local,)
    
    cursor.execute(query, params)
    resultado = cursor.fetchone()
    cursor.close()
    return resultado['total'] if resultado else 0
from db import consultar_todos, consultar_uno, ejecutar


def listar_locales():
    return consultar_todos("SELECT * FROM locales")


def buscar_local_por_id(id_local):
    return consultar_uno("SELECT * FROM locales WHERE id = %s", (id_local,))


def agregar_local(data):
    sql = "INSERT INTO locales (nombre, direccion) VALUES (%s, %s)"
    params = (data.get('nombre'), data.get('direccion'))
    id_creado, _ = ejecutar(sql, params)
    return id_creado


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
        return 0

    params.append(id_local)
    sql = f"UPDATE locales SET {', '.join(campos)} WHERE id = %s"
    _, filas_afectadas = ejecutar(sql, tuple(params))
    return filas_afectadas


def eliminar_local(id_local):
    _, filas_afectadas = ejecutar("DELETE FROM locales WHERE id = %s", (id_local,))
    return filas_afectadas


def contar_salas_de_local(id_local):
    resultado = consultar_uno("SELECT COUNT(*) AS total FROM salas WHERE id_local = %s", (id_local,))
    return resultado['total'] if resultado else 0
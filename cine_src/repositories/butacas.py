from db import consultar_todos, consultar_uno


def buscar_funcion_por_id(id_funcion):
    query = "SELECT * FROM funciones WHERE id = %s"
    return consultar_uno(query, (id_funcion,))


def listar_butacas_por_funcion(id_funcion):
    query = """
        SELECT 
            butacas.id,
            butacas.fila,
            butacas.columna,
            IF(entradas.id IS NOT NULL AND entradas.estado != 'cancelada', 'ocupada', 'disponible') AS estado
        FROM funciones
        JOIN butacas ON funciones.id_sala = butacas.id_sala
        LEFT JOIN entradas ON butacas.id = entradas.id_butaca AND entradas.id_funcion = funciones.id
        WHERE funciones.id = %s
        ORDER BY butacas.fila, butacas.columna
    """
    return consultar_todos(query, (id_funcion,))
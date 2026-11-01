from cine_src.db import obtener_conexion as conexion

def buscar_funcion_por_id(id_funcion):
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM funciones WHERE id = %s"
    cursor.execute(query, (id_funcion,))
    funcion = cursor.fetchone()
    cursor.close()
    return funcion


def listar_butacas_por_funcion(id_funcion):
    cursor = conexion.cursor(dictionary=True)

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

    cursor.execute(query, (id_funcion,))
    butacas = cursor.fetchall()
    cursor.close()

    return butacas
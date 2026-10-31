from cine_src.db import obtener_conexion

def obtener_reserva(identificador: int):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute('SELECT id, id_usuario, estado FROM reservas WHERE id = %s', (identificador,))
            return cursor.fetchone()
        finally:
            cursor.close()

def listar(identificador: int):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute('SELECT c.id, c.id_reserva, c.id_servicio, s.nombre, c.cantidad, c.precio_unitario, c.subtotal FROM consumos c JOIN servicios s ON s.id = c.id_servicio WHERE c.id_reserva = %s ORDER BY c.id', (identificador,))
            return cursor.fetchall()
        finally:
            cursor.close()

def agregar(id_reserva: int, id_usuario: int, id_servicio: int, cantidad: int):
    from cine_src.errors import ApiError
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            conexion.start_transaction()
            cursor.execute('SELECT id, id_usuario, estado FROM reservas WHERE id = %s FOR UPDATE', (id_reserva,))
            reserva = cursor.fetchone()
            if reserva is None:
                raise ApiError('La reserva no existe', 404)
            if reserva['id_usuario'] != id_usuario:
                raise ApiError('No podés modificar la reserva de otra persona', 403)
            if reserva['estado'] != 'pendiente':
                raise ApiError('La reserva ya no admite modificaciones', 409)
            cursor.execute('SELECT id, precio FROM servicios WHERE id = %s AND activo = 1', (id_servicio,))
            servicio = cursor.fetchone()
            if servicio is None:
                raise ApiError('El servicio no existe o está inactivo', 404)
            precio = servicio['precio']
            subtotal = precio * cantidad
            if subtotal > 2147483647:
                raise ApiError('El subtotal excede el límite permitido', 400)
            cursor.execute('INSERT INTO consumos (id_reserva, id_servicio, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)', (id_reserva, id_servicio, cantidad, precio, subtotal))
            id_consumo = cursor.lastrowid
            conexion.commit()
            return {'id': id_consumo, 'id_reserva': id_reserva, 'id_servicio': id_servicio, 'cantidad': cantidad, 'precio_unitario': precio, 'subtotal': subtotal}
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()

def eliminar(id_reserva: int, id_usuario: int, id_consumo: int):
    from cine_src.errors import ApiError
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            conexion.start_transaction()
            cursor.execute('SELECT id, id_usuario, estado FROM reservas WHERE id = %s FOR UPDATE', (id_reserva,))
            reserva = cursor.fetchone()
            if reserva is None:
                raise ApiError('La reserva no existe', 404)
            if reserva['id_usuario'] != id_usuario:
                raise ApiError('No podés modificar la reserva de otra persona', 403)
            if reserva['estado'] != 'pendiente':
                raise ApiError('La reserva ya no admite modificaciones', 409)
            cursor.execute('DELETE FROM consumos WHERE id = %s AND id_reserva = %s', (id_consumo, id_reserva))
            if cursor.rowcount == 0:
                raise ApiError('El consumo no existe en esa reserva', 404)
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()

import secrets
from datetime import datetime
from mysql.connector import IntegrityError
from cine_src.db import consultar_todos, consultar_uno, ejecutar, obtener_conexion
from cine_src.errors import ApiError

_SELECT_ENTRADA = (
    'SELECT e.id, e.id_reserva, r.id_usuario, e.id_funcion, f.fecha_hora AS fecha_hora_funcion, '
    'e.id_butaca, e.precio, e.estado, e.codigo_qr, e.fecha_hora_uso, e.fecha_hora_cancelacion, '
    'TIMESTAMPDIFF(MINUTE, NOW(), f.fecha_hora) AS minutos_restantes '
    'FROM entradas e JOIN reservas r ON r.id = e.id_reserva JOIN funciones f ON f.id = e.id_funcion '
)


def _serializar(fila):
    if fila is None:
        return None
    return {clave: (valor.isoformat() if isinstance(valor, datetime) else valor) for clave, valor in fila.items()}


def crear(id_usuario: int, id_funcion: int, butacas: list):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            conexion.start_transaction()
            # Bloquear la función evita que dos compras simultáneas elijan la misma butaca
            cursor.execute('SELECT id, id_sala, precio FROM funciones WHERE id = %s AND fecha_hora > NOW() FOR UPDATE', (id_funcion,))
            funcion = cursor.fetchone()
            if funcion is None:
                raise ApiError('La función no existe o ya comenzó', 404)
            marcas = ', '.join(['%s'] * len(butacas))
            cursor.execute(f'SELECT id FROM butacas WHERE id_sala = %s AND id IN ({marcas})', (funcion['id_sala'], *butacas))
            if len(cursor.fetchall()) != len(butacas):
                raise ApiError('Alguna butaca no existe en la sala de la función', 404)
            cursor.execute(f"SELECT id_butaca FROM entradas WHERE id_funcion = %s AND estado <> 'cancelada' AND id_butaca IN ({marcas})", (id_funcion, *butacas))
            ocupadas = sorted(fila['id_butaca'] for fila in cursor.fetchall())
            if ocupadas:
                raise ApiError('Butacas ya vendidas: ' + ', '.join(str(o) for o in ocupadas), 409)
            cursor.execute("INSERT INTO reservas (id_usuario, estado) VALUES (%s, 'pendiente')", (id_usuario,))
            id_reserva = cursor.lastrowid
            entradas = []
            for id_butaca in butacas:
                codigo = secrets.token_hex(16)
                cursor.execute('INSERT INTO entradas (id_reserva, id_funcion, id_butaca, codigo_qr, precio) VALUES (%s, %s, %s, %s, %s)', (id_reserva, id_funcion, id_butaca, codigo, funcion['precio']))
                entradas.append({'id': cursor.lastrowid, 'id_butaca': id_butaca, 'codigo_qr': codigo, 'precio': funcion['precio'], 'estado': 'activa'})
            conexion.commit()
            return {'id_reserva': id_reserva, 'id_funcion': id_funcion, 'total': funcion['precio'] * len(butacas), 'entradas': entradas}
        except IntegrityError:
            conexion.rollback()
            raise ApiError('Alguna butaca se vendió mientras comprabas', 409)
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()


def listar(id_usuario=None, id_funcion=None, estado=None):
    condiciones = []
    parametros = []
    if id_usuario is not None:
        condiciones.append('r.id_usuario = %s')
        parametros.append(id_usuario)
    if id_funcion is not None:
        condiciones.append('e.id_funcion = %s')
        parametros.append(id_funcion)
    if estado is not None:
        condiciones.append('e.estado = %s')
        parametros.append(estado)
    donde = ('WHERE ' + ' AND '.join(condiciones) + ' ') if condiciones else ''
    filas = consultar_todos(_SELECT_ENTRADA + donde + 'ORDER BY e.id DESC', tuple(parametros))
    return [_serializar(fila) for fila in filas]


def obtener(id_entrada: int):
    return _serializar(consultar_uno(_SELECT_ENTRADA + 'WHERE e.id = %s', (id_entrada,)))


def cancelar(id_entrada: int) -> bool:
    _, filas = ejecutar("UPDATE entradas SET estado = 'cancelada', fecha_hora_cancelacion = NOW() WHERE id = %s AND estado = 'activa'", (id_entrada,))
    return filas > 0


def buscar_por_codigo(codigo_qr: str):
    return consultar_uno('SELECT e.id, e.id_funcion, e.id_butaca, e.estado, DATE(f.fecha_hora) = CURDATE() AS es_hoy FROM entradas e JOIN funciones f ON f.id = e.id_funcion WHERE e.codigo_qr = %s', (codigo_qr,))


def marcar_usada(id_entrada: int) -> bool:
    _, filas = ejecutar("UPDATE entradas SET estado = 'usada', fecha_hora_uso = NOW() WHERE id = %s AND estado = 'activa'", (id_entrada,))
    return filas > 0

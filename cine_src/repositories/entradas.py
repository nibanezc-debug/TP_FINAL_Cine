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

def _donde(condiciones: list) -> str:
    return ('WHERE ' + ' AND '.join(condiciones) + ' ') if condiciones else ''

def _serializar(fila):
    if fila is None:
        return None
    return {clave: (valor.isoformat() if isinstance(valor, datetime) else valor) for clave, valor in fila.items()}

def crear(id_usuario: int, id_funcion: int, butacas: list):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            conexion.start_transaction()
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
    filas = consultar_todos(_SELECT_ENTRADA + _donde(condiciones) + 'ORDER BY e.id DESC', tuple(parametros))
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

def obtener_usuario(id_usuario: int):
    return consultar_uno('SELECT id_usuarios AS id, nombre, email FROM usuarios WHERE id_usuarios = %s', (id_usuario,))

def obtener_factura(id_reserva: int):
    reserva = consultar_uno('SELECT r.id AS id_reserva, u.nombre, u.email FROM reservas r JOIN usuarios u ON u.id_usuarios = r.id_usuario WHERE r.id = %s', (id_reserva,))
    if reserva is None:
        return None
    entradas = consultar_todos('SELECT e.id, e.id_funcion, f.fecha_hora AS fecha_hora_funcion, e.id_butaca, e.precio, e.estado FROM entradas e JOIN funciones f ON f.id = e.id_funcion WHERE e.id_reserva = %s ORDER BY e.id', (id_reserva,))
    servicios = consultar_todos('SELECT c.id, s.nombre, c.cantidad, c.precio_unitario, c.subtotal FROM consumos c JOIN servicios s ON s.id = c.id_servicio WHERE c.id_reserva = %s ORDER BY c.id', (id_reserva,))
    return {'reserva': reserva, 'entradas': [_serializar(e) for e in entradas], 'servicios': servicios}

def _condiciones_periodo(periodo: dict) -> tuple:
    condiciones = []
    parametros = []
    if 'desde' in periodo:
        condiciones.append('f.fecha_hora >= %s')
        parametros.append(periodo['desde'])
    if 'hasta' in periodo:
        condiciones.append('f.fecha_hora < DATE_ADD(%s, INTERVAL 1 DAY)')
        parametros.append(periodo['hasta'])
    return condiciones, parametros

_AGRUPACIONES = {
    'funcion': ('e.id_funcion, f.fecha_hora AS fecha_hora_funcion', '', 'e.id_funcion, f.fecha_hora'),
    'pelicula': ('p.id AS id_pelicula, p.titulo', 'JOIN peliculas p ON p.id = f.id_pelicula ', 'p.id, p.titulo'),
}

def cancelaciones(agrupar: str, periodo: dict):
    columnas, union, grupo = _AGRUPACIONES[agrupar]
    condiciones, parametros = _condiciones_periodo(periodo)
    sql = (f"SELECT {columnas}, COUNT(*) AS entradas, CAST(SUM(e.estado = 'cancelada') AS UNSIGNED) AS cancelaciones "
           f'FROM entradas e JOIN funciones f ON f.id = e.id_funcion {union}{_donde(condiciones)}'
           f'GROUP BY {grupo} HAVING cancelaciones > 0 ORDER BY cancelaciones DESC')
    return [_serializar(fila) for fila in consultar_todos(sql, tuple(parametros))]

def franjas_horarias(periodo: dict):
    condiciones, parametros = _condiciones_periodo(periodo)
    condiciones.append("e.estado <> 'cancelada'")
    sql = ('SELECT HOUR(f.fecha_hora) AS hora, COUNT(*) AS entradas, CAST(SUM(e.precio) AS UNSIGNED) AS recaudado '
           f'FROM entradas e JOIN funciones f ON f.id = e.id_funcion {_donde(condiciones)}'
           'GROUP BY HOUR(f.fecha_hora) ORDER BY entradas DESC, hora')
    return consultar_todos(sql, tuple(parametros))

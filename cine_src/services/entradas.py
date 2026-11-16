import io
import correo
from errors import ApiError
from repositories import entradas as repositorio
from validators.entradas import (validar_agrupacion, validar_compra, validar_estado, validar_filtros,
                                          validar_id, validar_periodo, validar_validacion)

MINUTOS_LIMITE_CANCELACION = 120

def _resumen(entrada: dict) -> dict:
    return {clave: valor for clave, valor in entrada.items() if clave not in ('codigo_qr', 'minutos_restantes')}

def _detalle(entrada: dict) -> dict:
    return {clave: valor for clave, valor in entrada.items() if clave != 'minutos_restantes'}

def _obtener_autorizado(id_entrada: int, usuario: dict) -> dict:
    validar_id(id_entrada)
    entrada = repositorio.obtener(id_entrada)
    if entrada is None:
        raise ApiError('La entrada no existe', 404)
    if entrada['id_usuario'] != usuario['id'] and usuario['rol'] != 'administrador':
        raise ApiError('No podés acceder a esta entrada', 403)
    return entrada

def _png_qr(codigo: str) -> bytes:
    import qrcode
    buffer = io.BytesIO()
    qrcode.make(codigo).save(buffer, format='PNG')
    return buffer.getvalue()

def _obtener_activa(id_entrada: int, usuario: dict) -> dict:
    entrada = _obtener_autorizado(id_entrada, usuario)
    if entrada['estado'] != 'activa':
        raise ApiError('La entrada ya no está activa', 409)
    return entrada

def comprar(usuario: dict, datos):
    if usuario['rol'] != 'cliente':
        raise ApiError('Solo un cliente puede comprar entradas', 403)
    compra = validar_compra(datos)
    return repositorio.crear(usuario['id'], compra['id_funcion'], compra['butacas'])

def listar(argumentos):
    filtros = validar_filtros(argumentos)
    return [_resumen(e) for e in repositorio.listar(filtros.get('id_usuario'), filtros.get('id_funcion'), filtros.get('estado'))]

def listar_mias(usuario: dict, argumentos):
    estado = argumentos.get('estado')
    if estado is not None:
        validar_estado(estado)
    return [_resumen(e) for e in repositorio.listar(id_usuario=usuario['id'], estado=estado)]

def obtener(id_entrada: int, usuario: dict):
    return _detalle(_obtener_autorizado(id_entrada, usuario))

def generar_qr(id_entrada: int, usuario: dict) -> bytes:
    return _png_qr(_obtener_activa(id_entrada, usuario)['codigo_qr'])

def factura(id_entrada: int, usuario: dict):
    entrada = _obtener_autorizado(id_entrada, usuario)
    datos = repositorio.obtener_factura(entrada['id_reserva'])
    if datos is None:
        raise ApiError('La reserva de la entrada no existe', 404)
    total_entradas = sum(e['precio'] for e in datos['entradas'] if e['estado'] != 'cancelada')
    total_servicios = sum(s['subtotal'] for s in datos['servicios'])
    return {**datos, 'total_entradas': total_entradas, 'total_servicios': total_servicios, 'total': total_entradas + total_servicios}

def pagar(id_entrada: int, usuario: dict):
    entrada = _obtener_autorizado(id_entrada, usuario)
    if entrada['estado'] != 'activa':
        raise ApiError('La entrada ya no está activa', 409)
    reserva = repositorio.obtener_reserva(entrada['id_reserva'])
    if reserva is None:
        raise ApiError('La reserva de la entrada no existe', 404)
    if reserva['estado'] != 'pendiente':
        raise ApiError('La reserva ya fue pagada o cancelada', 409)
    destinatario = repositorio.obtener_usuario(entrada['id_usuario'])
    if destinatario is None:
        raise ApiError('El usuario de la entrada no existe', 404)
    datos_factura = repositorio.obtener_factura(entrada['id_reserva'])
    entradas = repositorio.entradas_de_reserva(entrada['id_reserva'])
    adjuntos_qr = [(e['id'], _png_qr(e['codigo_qr'])) for e in entradas if e['estado'] == 'activa']
    correo.enviar_compra(destinatario, datos_factura, adjuntos_qr)
    if not repositorio.pagar_reserva(entrada['id_reserva']):
        raise ApiError('La reserva ya fue pagada o cancelada', 409)
    return {'pagada': True, 'id_reserva': entrada['id_reserva'], 'enviado': True, 'destinatario': destinatario['email']}

def reenviar(id_entrada: int, usuario: dict):
    entrada = _obtener_activa(id_entrada, usuario)
    destinatario = repositorio.obtener_usuario(entrada['id_usuario'])
    if destinatario is None:
        raise ApiError('El usuario de la entrada no existe', 404)
    correo.enviar_entrada(destinatario, entrada, _png_qr(entrada['codigo_qr']))
    return {'enviado': True, 'destinatario': destinatario['email']}

def cancelar(id_entrada: int, usuario: dict):
    entrada = _obtener_autorizado(id_entrada, usuario)
    if entrada['estado'] != 'activa':
        raise ApiError('La entrada ya fue usada o cancelada', 409)
    if entrada['minutos_restantes'] < MINUTOS_LIMITE_CANCELACION:
        raise ApiError('Ya pasó el plazo para cancelar esta entrada', 422)
    if not repositorio.cancelar(id_entrada):
        raise ApiError('La entrada ya fue usada o cancelada', 409)
    return _detalle(repositorio.obtener(id_entrada))

def validar(datos):
    codigo, id_funcion = validar_validacion(datos)
    entrada = repositorio.buscar_por_codigo(codigo)
    if entrada is None:
        raise ApiError('El código QR no corresponde a ninguna entrada', 404)
    if entrada['estado'] == 'usada':
        raise ApiError('La entrada ya fue utilizada', 409)
    if entrada['estado'] == 'cancelada':
        raise ApiError('La entrada fue cancelada', 409)
    if entrada['id_funcion'] != id_funcion:
        raise ApiError('La entrada es de otra función', 422)
    if not entrada['es_hoy']:
        raise ApiError('La entrada no corresponde a la fecha de hoy', 422)
    if not repositorio.marcar_usada(entrada['id']):
        raise ApiError('La entrada ya fue utilizada', 409)
    return {'valida': True, 'id': entrada['id'], 'id_butaca': entrada['id_butaca'], 'estado': 'usada'}

def estadisticas_cancelaciones(argumentos):
    filas = repositorio.cancelaciones(validar_agrupacion(argumentos), validar_periodo(argumentos))
    return [{**fila, 'porcentaje': round(fila['cancelaciones'] * 100 / fila['entradas'], 1)} for fila in filas]

def estadisticas_ocupacion(argumentos):
    return repositorio.ocupacion(validar_agrupacion(argumentos), validar_periodo(argumentos))

def estadisticas_ventas_genero(argumentos):
    return repositorio.ventas_por_genero(validar_periodo(argumentos))

def estadisticas_franjas(argumentos):
    filas = repositorio.franjas_horarias(validar_periodo(argumentos))
    return [{**fila, 'franja': f"{fila['hora']:02d}:00-{fila['hora']:02d}:59"} for fila in filas]

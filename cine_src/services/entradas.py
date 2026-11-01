import io
from cine_src.errors import ApiError
from cine_src.repositories import entradas as repositorio
from cine_src.validators.entradas import validar_compra, validar_filtros, validar_estado, validar_id, validar_validacion

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
    import qrcode
    entrada = _obtener_autorizado(id_entrada, usuario)
    if entrada['estado'] != 'activa':
        raise ApiError('La entrada ya no está activa', 409)
    buffer = io.BytesIO()
    qrcode.make(entrada['codigo_qr']).save(buffer, format='PNG')
    return buffer.getvalue()

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

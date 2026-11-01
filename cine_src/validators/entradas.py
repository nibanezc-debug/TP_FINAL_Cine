from datetime import datetime
from cine_src.errors import ApiError

ESTADOS = ('activa', 'usada', 'cancelada')

def validar_id(valor, nombre: str = 'id') -> int:
    if type(valor) is not int or valor <= 0:
        raise ApiError(f'El {nombre} debe ser un entero positivo', 400)
    return valor

def validar_estado(estado) -> str:
    if estado not in ESTADOS:
        raise ApiError('El estado debe ser activa, usada o cancelada', 400)
    return estado

def validar_compra(datos) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    id_funcion = validar_id(datos.get('id_funcion'), 'id_funcion')
    butacas = datos.get('butacas')
    if not isinstance(butacas, list) or not butacas:
        raise ApiError('Debés elegir al menos una butaca', 400)
    for id_butaca in butacas:
        validar_id(id_butaca, 'id de butaca')
    if len(set(butacas)) != len(butacas):
        raise ApiError('Hay butacas repetidas', 400)
    return {'id_funcion': id_funcion, 'butacas': butacas}

def validar_validacion(datos) -> tuple:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    codigo = datos.get('codigo_qr')
    if not isinstance(codigo, str) or not codigo.strip() or len(codigo.strip()) > 64:
        raise ApiError('El código QR es obligatorio', 400)
    id_funcion = validar_id(datos.get('id_funcion'), 'id_funcion')
    return codigo.strip(), id_funcion

def validar_filtros(argumentos) -> dict:
    filtros = {}
    for clave in ('id_funcion', 'id_usuario'):
        valor = argumentos.get(clave)
        if valor is not None:
            if not valor.isdigit() or int(valor) <= 0:
                raise ApiError(f'El filtro {clave} debe ser un entero positivo', 400)
            filtros[clave] = int(valor)
    estado = argumentos.get('estado')
    if estado is not None:
        filtros['estado'] = validar_estado(estado)
    return filtros

AGRUPACIONES = ('funcion', 'pelicula')

def validar_agrupacion(argumentos) -> str:
    agrupar = argumentos.get('agrupar', 'funcion')
    if agrupar not in AGRUPACIONES:
        raise ApiError('El parámetro agrupar debe ser funcion o pelicula', 400)
    return agrupar

def _validar_fecha(valor: str, nombre: str) -> str:
    try:
        return datetime.strptime(valor, '%Y-%m-%d').date().isoformat()
    except ValueError:
        raise ApiError(f'El parámetro {nombre} debe tener formato AAAA-MM-DD', 400)

def validar_periodo(argumentos) -> dict:
    periodo = {}
    for clave in ('desde', 'hasta'):
        valor = argumentos.get(clave)
        if valor:
            periodo[clave] = _validar_fecha(valor, clave)
    if 'desde' in periodo and 'hasta' in periodo and periodo['desde'] > periodo['hasta']:
        raise ApiError('La fecha desde no puede ser posterior a la fecha hasta', 400)
    return periodo

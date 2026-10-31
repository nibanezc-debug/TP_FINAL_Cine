from cine_src.errors import ApiError
from cine_src.repositories import consumos as repositorio
from cine_src.validators.servicios import validar_id

def _validar_propietario(id_reserva: int, usuario: dict, permitir_admin: bool):
    reserva = repositorio.obtener_reserva(id_reserva)
    if reserva is None:
        raise ApiError('La reserva no existe', 404)
    if reserva['id_usuario'] != usuario['id']:
        if not permitir_admin or usuario['rol'] != 'administrador':
            raise ApiError('No podés acceder a esta reserva', 403)
    return reserva

def listar(id_reserva: int, usuario: dict):
    validar_id(id_reserva)
    _validar_propietario(id_reserva, usuario, permitir_admin=True)
    return repositorio.listar(id_reserva)

def agregar(id_reserva: int, usuario: dict, datos):
    validar_id(id_reserva)
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    id_servicio = datos.get('id_servicio')
    cantidad = datos.get('cantidad')
    validar_id(id_servicio)
    if type(cantidad) is not int or cantidad <= 0:
        raise ApiError('La cantidad debe ser un entero positivo', 400)
    if usuario['rol'] != 'cliente':
        raise ApiError('Solo un cliente puede agregar consumos a su reserva', 403)
    return repositorio.agregar(id_reserva, usuario['id'], id_servicio, cantidad)

def eliminar(id_reserva: int, id_consumo: int, usuario: dict):
    validar_id(id_reserva)
    validar_id(id_consumo)
    if usuario['rol'] != 'cliente':
        raise ApiError('Solo un cliente puede quitar consumos de su reserva', 403)
    repositorio.eliminar(id_reserva, usuario['id'], id_consumo)

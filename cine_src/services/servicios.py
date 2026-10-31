from cine_src.errors import ApiError
from cine_src.repositories import servicios as repositorio
from cine_src.validators.servicios import validar_servicio, validar_id

def listar():
    return repositorio.listar()

def buscar(identificador):
    validar_id(identificador)
    servicio = repositorio.buscar(identificador)
    if servicio is None:
        raise ApiError('El servicio solicitado no existe', 404)
    return servicio

def crear(datos):
    servicio = validar_servicio(datos)
    identificador = repositorio.insertar(servicio['nombre'], servicio['precio'])
    return buscar(identificador)

def actualizar(identificador, datos):
    buscar(identificador)
    servicio = validar_servicio(datos)
    repositorio.actualizar(identificador, servicio['nombre'], servicio['precio'])
    return buscar(identificador)

def eliminar(identificador):
    buscar(identificador)
    repositorio.desactivar(identificador)

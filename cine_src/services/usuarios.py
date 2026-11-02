from flask import session
from cine_src.errors import ApiError
from cine_src.repositories import usuarios as repositorio
from cine_src.validators.usuarios import (
    validar_id,
    validar_registro,
    validar_login,
    validar_actualizacion
)

def _validar_permiso_usuario_o_admin(id_usuario: int, usuario_actual: dict):
    if not usuario_actual:
        raise ApiError("Usuario no autenticado", 401)
    
    es_admin = usuario_actual.get('rol') == 'administrador'
    es_propio = (usuario_actual.get('id') == id_usuario) or (usuario_actual.get('id_usuario') == id_usuario)
    
    if not es_admin and not es_propio:
        raise ApiError('No tenés permisos para acceder a estos datos', 403)

def registrar(datos: dict) -> dict:
    datos_validos = validar_registro(datos)
    id_nuevo = repositorio.crear_usuario(
        datos_validos['nombre'],
        datos_validos['email'],
        datos_validos['password']
    )
    return {
        'mensaje': 'Usuario registrado exitosamente',
        'id_usuario': id_nuevo
    }


def login(datos: dict) -> dict:
    datos_validos = validar_login(datos)
    usuario = repositorio.buscar_por_email(datos_validos['email'])
    
    if not usuario or usuario['password'] != datos_validos['password']:
        raise ApiError('Credenciales inválidas', 401)
        
    session['id_usuario'] = usuario['id']
    session['rol'] = usuario['rol']
    
    return {
        'id_usuario': usuario['id'],
        'nombre': usuario['nombre'],
        'email': usuario['email'],
        'rol': usuario['rol']
    }
    
def logout():
    session.clear()
    
def obtener_por_id(id_usuario: int, usuario_actual: dict) -> dict:
    id_valido = validar_id(id_usuario)
    _validar_permiso_usuario_o_admin(id_valido, usuario_actual)
    
    usuario = repositorio.buscar_por_id(id_valido)
    if not usuario:
        raise ApiError('El usuario no existe', 404)
    
    usuario.pop('password', None)
    return usuario

def actualizar_perfil(id_usuario: int, usuario_actual: dict, datos: dict) -> dict:
    id_valido = validar_id(id_usuario)
    _validar_permiso_usuario_o_admin(id_valido, usuario_actual)
    datos_validos = validar_actualizacion(datos)
    
    usuario = repositorio.buscar_por_id(id_valido)
    if not usuario:
        raise ApiError('El usuario no existe', 404)
        
    nombre = datos_validos.get('nombre', usuario['nombre'])
    email = datos_validos.get('email', usuario['email'])
    
    repositorio.actualizar_usuario(id_valido, nombre, email)
    return {'mensaje': 'Perfil actualizado correctamente'}

def listar_todos():
    usuarios = repositorio.listar_todos()
    for u in usuarios:
        u.pop('password', None)
    return usuarios

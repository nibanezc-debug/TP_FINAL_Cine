from flask import session
from cine_src.errors import ApiError
from cine_src.repositories import usuarios as repositorio

def _validar_permiso_usuario_o_admin(id_usuario: int, usuario_actual: dict):
    if not usuario_actual:
        raise ApiError("Usuario no autenticado", 401)
    
    es_admin = usuario_actual.get('rol') == 'administrador'
    es_propio = (usuario_actual.get('id') == id_usuario) or (usuario_actual.get('id_usuario') == id_usuario)
    
    if not es_admin and not es_propio:
        raise ApiError('No tenés permisos para acceder a estos datos', 403)

def registrar(datos: dict) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ApiError('El cuerpo debe ser un objeto JSON válido')
    
    nombre = datos.get('nombre')
    email = datos.get('email')
    password = datos.get('password')
    
    if not nombre or not email or not password:
        raise ApiError('Los campos nombre, email y password son obligatorios', 400)
    
    id_nuevo = repositorio.crear_usuario(nombre, email, password)
    return {
        'mensaje': 'Usuario registrado exitosamente',
        'id_usuario': id_nuevo
    }


def login(datos: dict) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ApiError('El cuerpo debe ser un objeto JSON válido')
    
    email = datos.get('email')
    password = datos.get('password')
    
    if not email or not password:
        raise ApiError('Debe ingresar email y contraseña', 400)
    
    usuario = repositorio.buscar_por_email(email)
    if not usuario or usuario['password'] != password:
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
    _validar_permiso_usuario_o_admin(id_usuario, usuario_actual)
    usuario = repositorio.buscar_por_id(id_usuario)
    if not usuario:
        raise ApiError('El usuario no existe', 404)
    
    usuario.pop('password', None)
    return usuario

def actualizar_perfil(id_usuario: int, usuario_actual: dict, datos: dict) -> dict:
    _validar_permiso_usuario_o_admin(id_usuario, usuario_actual)
    if not isinstance(datos, dict) or not datos:
        raise ApiError('Debe enviar un objeto JSON con los datos a actualizar', 400)
    usuario = repositorio.buscar_por_id(id_usuario)
    if not usuario:
        raise ApiError('El usuario no existe', 404)
    nombre = datos.get('nombre', usuario['nombre'])
    email = datos.get('email', usuario['email'])
    repositorio.actualizar_usuario(id_usuario, nombre, email)
    return {'mensaje': 'Perfil actualizado correctamente'}

def listar_todos():
    usuarios = repositorio.listar_todos()
    for u in usuarios:
        u.pop('password', None)
    return usuarios

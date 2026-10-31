from functools import wraps
from flask import request, session
from werkzeug.security import check_password_hash
from cine_src.db import consultar_uno
from cine_src.errors import ApiError

def usuario_actual() -> dict:
    id_usuario = session.get('id_usuario')
    if type(id_usuario) is int and id_usuario > 0:
        usuario = consultar_uno('SELECT id_usuarios AS id, rol FROM usuarios WHERE id_usuarios = %s', (id_usuario,))
        if usuario:
            return usuario
    credenciales = request.authorization
    if credenciales and (credenciales.type or '').lower() == 'basic':
        if not request.is_secure and request.remote_addr not in ('127.0.0.1', '::1'):
            raise ApiError('HTTP Basic solo está permitido con HTTPS o en localhost', 403)
        usuario = consultar_uno('SELECT id_usuarios AS id, rol, password_hash FROM usuarios WHERE email = %s', (credenciales.username,))
        if usuario and check_password_hash(usuario['password_hash'], credenciales.password or ''):
            return {'id': usuario['id'], 'rol': usuario['rol']}
    raise ApiError('Debés iniciar sesión para utilizar este endpoint', 401)

def requiere_usuario(funcion):

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        usuario_actual()
        return funcion(*args, **kwargs)
    return envoltura

def requiere_admin(funcion):

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        usuario = usuario_actual()
        if usuario['rol'] != 'administrador':
            raise ApiError('No tenés permisos de administrador', 403)
        return funcion(*args, **kwargs)
    return envoltura

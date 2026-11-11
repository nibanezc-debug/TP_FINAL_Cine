from flask import Blueprint, jsonify, request
from security import requiere_admin, requiere_usuario, usuario_actual
from services import usuarios as servicio

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.post('/auth/register')
def registrar():
    datos = request.get_json(silent=True) or {}
    nuevo_usuario = servicio.registrar(datos)
    return jsonify(nuevo_usuario), 201

@usuarios_bp.post('/auth/login')
def login():
    datos = request.get_json(silent=True) or {}
    respuesta = servicio.login(datos)
    return jsonify(respuesta), 200

@usuarios_bp.post('/auth/logout')
@requiere_usuario
def logout():
    servicio.logout()
    return jsonify({'mensaje': 'Sesión cerrada correctamente'}), 200


@usuarios_bp.get('/usuarios/<int:id_usuario>')
@requiere_usuario
def obtener_usuario(id_usuario):
    usuario = servicio.obtener_por_id(id_usuario, usuario_actual())
    return jsonify(usuario), 200


@usuarios_bp.put('/usuarios/<int:id_usuario>')
@requiere_usuario
def actualizar_usuario(id_usuario):
    datos = request.get_json(silent=True) or {}
    usuario_actualizado = servicio.actualizar_perfil(id_usuario, usuario_actual(), datos)
    return jsonify(usuario_actualizado), 200

@usuarios_bp.get('/usuarios')
@requiere_admin
def listar_usuarios():
    lista = servicio.listar_todos()
    return jsonify(lista), 200
from flask import Blueprint, Response, jsonify, request
from cine_src.security import requiere_admin, usuario_actual
from cine_src.services import entradas as servicio

entradas_bp = Blueprint('entradas', __name__)

@entradas_bp.post('/entradas')
def comprar_entradas():
    return (jsonify(servicio.comprar(usuario_actual(), request.get_json(silent=True))), 201)

@entradas_bp.get('/entradas')
@requiere_admin
def listar_entradas():
    return (jsonify(servicio.listar(request.args)), 200)

@entradas_bp.get('/entradas/mias')
def listar_mis_entradas():
    return (jsonify(servicio.listar_mias(usuario_actual(), request.args)), 200)

@entradas_bp.get('/entradas/<int:id_entrada>')
def obtener_entrada(id_entrada):
    return (jsonify(servicio.obtener(id_entrada, usuario_actual())), 200)

@entradas_bp.get('/entradas/<int:id_entrada>/qr')
def obtener_qr(id_entrada):
    return Response(servicio.generar_qr(id_entrada, usuario_actual()), mimetype='image/png')

@entradas_bp.patch('/entradas/<int:id_entrada>/cancelar')
def cancelar_entrada(id_entrada):
    return (jsonify(servicio.cancelar(id_entrada, usuario_actual())), 200)

@entradas_bp.post('/entradas/validar')
@requiere_admin
def validar_entrada():
    return (jsonify(servicio.validar(request.get_json(silent=True))), 200)

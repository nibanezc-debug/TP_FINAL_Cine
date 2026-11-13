from flask import Blueprint, Response, jsonify, request
from security import requiere_admin, usuario_actual
from services import entradas as servicio

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

@entradas_bp.get('/entradas/<int:id_entrada>/factura')
def obtener_factura(id_entrada):
    return (jsonify(servicio.factura(id_entrada, usuario_actual())), 200)

@entradas_bp.post('/entradas/<int:id_entrada>/pagar')
def pagar_entrada(id_entrada):
    return (jsonify(servicio.pagar(id_entrada, usuario_actual())), 200)

@entradas_bp.post('/entradas/<int:id_entrada>/reenviar')
def reenviar_entrada(id_entrada):
    return (jsonify(servicio.reenviar(id_entrada, usuario_actual())), 200)

@entradas_bp.get('/entradas/estadisticas/cancelaciones')
@requiere_admin
def estadisticas_cancelaciones():
    return (jsonify(servicio.estadisticas_cancelaciones(request.args)), 200)

@entradas_bp.get('/entradas/estadisticas/ocupacion')
@requiere_admin
def estadisticas_ocupacion():
    return (jsonify(servicio.estadisticas_ocupacion(request.args)), 200)

@entradas_bp.get('/entradas/estadisticas/ventas-genero')
@requiere_admin
def estadisticas_ventas_genero():
    return (jsonify(servicio.estadisticas_ventas_genero(request.args)), 200)

@entradas_bp.get('/entradas/estadisticas/franjas-horarias')
@requiere_admin
def estadisticas_franjas_horarias():
    return (jsonify(servicio.estadisticas_franjas(request.args)), 200)

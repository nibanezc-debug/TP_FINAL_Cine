from flask import Blueprint, jsonify, request
from cine_src.security import requiere_admin, requiere_usuario
from cine_src.services import servicios as servicio
servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.get('/servicios')
@requiere_usuario
def listar_servicios():
    return (jsonify(servicio.listar()), 200)

@servicios_bp.get('/servicios/<int:id_servicio>')
@requiere_usuario
def obtener_servicio(id_servicio):
    return (jsonify(servicio.buscar(id_servicio)), 200)

@servicios_bp.post('/servicios')
@requiere_admin
def crear_servicio():
    return (jsonify(servicio.crear(request.get_json(silent=True))), 201)

@servicios_bp.put('/servicios/<int:id_servicio>')
@requiere_admin
def modificar_servicio(id_servicio):
    return (jsonify(servicio.actualizar(id_servicio, request.get_json(silent=True))), 200)

@servicios_bp.delete('/servicios/<int:id_servicio>')
@requiere_admin
def eliminar_servicio(id_servicio):
    servicio.eliminar(id_servicio)
    return ('', 204)

from flask import Blueprint, jsonify, request
from cine_src.security import usuario_actual
from cine_src.services import consumos as servicio
consumos_bp = Blueprint('consumos', __name__)

@consumos_bp.get('/reservas/<int:id_reserva>/consumos')
def listar_consumos(id_reserva):
    return (jsonify(servicio.listar(id_reserva, usuario_actual())), 200)

@consumos_bp.post('/reservas/<int:id_reserva>/consumos')
def agregar_consumo(id_reserva):
    datos = request.get_json(silent=True)
    return (jsonify(servicio.agregar(id_reserva, usuario_actual(), datos)), 201)

@consumos_bp.delete('/reservas/<int:id_reserva>/consumos/<int:id_consumo>')
def eliminar_consumo(id_reserva, id_consumo):
    servicio.eliminar(id_reserva, id_consumo, usuario_actual())
    return ('', 204)

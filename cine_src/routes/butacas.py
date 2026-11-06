from flask import Blueprint, jsonify, request
from repositories import butacas as repositories

butacas_bp = Blueprint('butacas_bp', __name__)

@butacas_bp.route('/funciones/<int:id_funcion>/butacas', methods=['GET'])
def get_butacas_por_funcion(id_funcion):
    if repositories.buscar_funcion_por_id(id_funcion) is None:
        return jsonify({'error': 'Funcion no encontrada'}), 404

    butacas = repositories.listar_butacas_por_funcion(id_funcion)

    return jsonify(butacas or []), 200
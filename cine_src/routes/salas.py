from flask import Blueprint, jsonify
from repositories import salas as repositories
from services import salas as services
from security import requiere_admin

salas_bp = Blueprint('salas_bp', __name__)

@salas_bp.route('/locales/<int:id_local>/salas', methods=['GET'])
def get_salas_por_local(id_local):
    if repositories.buscar_local_por_id(id_local) is None:
        return jsonify({'error': 'Local no encontrado'}), 404

    respuesta = services.obtener_salas_por_local_paginado(id_local, request.args)
    return jsonify(respuesta), 200



@salas_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
@requiere_admin
def delete_sala(id_sala):
    if repositories.buscar_sala_por_id(id_sala) is None:
        return jsonify({'error': 'no existe esta sala'}), 404

    if services.sala_activa(id_sala):
        return jsonify({'error': 'la sala esta en uso por una funcion, puede modificar funcion con PATCH'}), 409

    repositories.eliminar_sala(id_sala)
    return '', 204
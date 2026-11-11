from flask import Blueprint, jsonify, request
from repositories import locales as repositories
from services import locales as services
from security import requiere_admin

locales_bp = Blueprint('locales_bp', __name__)

@locales_bp.route('/locales', methods=['GET'])
def get_locales():
    try:
        locales = repositories.listar_locales()
        return jsonify(locales), 200
    except Exception as e:
        print("\n---> ERROR REAL DE MYSQL:", str(e), "\n")
        return jsonify({"error": str(e)}), 500

@locales_bp.route('/locales', methods=['POST'])
@requiere_admin
def post_locales():
    data = request.get_json(silent=True) or {}
    
    es_valido, mensaje, codigo = services.validar_data_locales(data)
    if not es_valido:    
        return jsonify(mensaje), codigo

    repositories.agregar_local(data)
    return jsonify({'message': 'Local agregado exitosamente'}), 201


@locales_bp.route('/locales/<int:id_local>', methods=['PATCH'])
@requiere_admin
def patch_locales(id_local):
    if repositories.buscar_local_por_id(id_local) is None:
        return jsonify({'error': 'no existe este local'}), 404
    
    data = request.get_json(silent=True) or {}

    es_valido, mensaje, codigo = services.validar_data_locales(data, es_patch=True)
    if not es_valido:
        return jsonify(mensaje), codigo

    repositories.actualizar_local(data, id_local)
    return '', 204


@locales_bp.route('/locales/<int:id_local>', methods=['DELETE'])
@requiere_admin
def delete_local(id_local):
    if repositories.buscar_local_por_id(id_local) is None:
        return jsonify({'error': 'no existe este local'}), 404

    if services.local_tiene_salas(id_local):
        return jsonify({'error': 'el local posee salas asociadas, debe eliminarlas antes'}), 409

    repositories.eliminar_local(id_local)
    return '', 204
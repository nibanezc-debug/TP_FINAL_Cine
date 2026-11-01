from flask import Blueprint, jsonify, request
from cine_src.repositories import salas as repositories
from cine_src.services import salas as services
from cine_src.security import requiere_admin

salas_bp = Blueprint('salas_bp', __name__)

@salas_bp.route('/locales/<int:id_local>/salas', methods=['GET'])
def get_salas_por_local(id_local):
    if repositories.buscar_local_por_id(id_local) is None:
        return jsonify({'error': 'Local no encontrado'}), 404

    # Parámetros de filtro
    formato = request.args.get('formato')
    capacidad = request.args.get('capacidad', type=int)

    # Parámetros de paginación con guión bajo
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    # El servicio devuelve la lista paginada y el conteo total de registros
    salas, total = services.listar_salas_por_local(
        id_local=id_local, 
        formato=formato, 
        capacidad=capacidad,
        limit=limit,
        offset=offset
    )

    # Construcción de query params para preservar filtros en los links HATEOAS
    extra_params = ""
    if formato:
        extra_params += f"&formato={formato}"
    if capacidad is not None:
        extra_params += f"&capacidad={capacidad}"

    base_url = request.base_url

    # Cálculo de los offsets para navegación HATEOAS
    prev_offset = offset - limit if offset - limit >= 0 else None
    next_offset = offset + limit if (offset + limit) < total else None
    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0

    response = {
        'items': salas or [],
        '_limit': limit,
        '_offset': offset,
        '_total': total,
        '_first': f"{base_url}?_limit={limit}&_offset=0{extra_params}",
        '_prev': f"{base_url}?_limit={limit}&_offset={prev_offset}{extra_params}" if prev_offset is not None else None,
        '_next': f"{base_url}?_limit={limit}&_offset={next_offset}{extra_params}" if next_offset is not None else None,
        '_last': f"{base_url}?_limit={limit}&_offset={last_offset}{extra_params}"
    }

    return jsonify(response), 200


@salas_bp.route('/locales/<int:id_local>/salas', methods=['POST'])
@requiere_admin
def post_sala_por_local(id_local):
    if repositories.buscar_local_por_id(id_local) is None:
        return jsonify({'error': 'Local no encontrado'}), 404

    data = request.get_json(silent=True) or {}

    es_valido, mensaje, codigo = services.validar_data_salas(data)
    if not es_valido:    
        return jsonify(mensaje), codigo

    repositories.agregar_sala(data, id_local)
    return jsonify({'message': 'Sala agregada exitosamente'}), 201


@salas_bp.route('/salas/<int:id_sala>', methods=['PATCH'])
@requiere_admin
def patch_sala_por_local(id_sala): 
    if repositories.buscar_sala_por_id(id_sala) is None:
        return jsonify({'error': 'no existe esta sala'}), 404
    
    data = request.get_json(silent=True) or {}

    es_valido, mensaje, codigo = services.validar_data_salas(data, es_patch=True)
    if not es_valido:
        return jsonify(mensaje), codigo

    repositories.actualizar_sala(data, id_sala)
    return '', 204


@salas_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
@requiere_admin
def delete_sala(id_sala):
    if repositories.buscar_sala_por_id(id_sala) is None:
        return jsonify({'error': 'no existe esta sala'}), 404

    if services.sala_activa(id_sala):
        return jsonify({'error': 'la sala esta en uso por una funcion, puede modificar funcion con PATCH'}), 409

    repositories.eliminar_sala(id_sala)
    return '', 204
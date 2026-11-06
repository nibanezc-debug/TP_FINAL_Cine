from flask import Blueprint, jsonify, request
from validators import peliculas as peliculas_validator
from services import peliculas as peliculas_service
from security import requiere_admin, requiere_usuario, usuario_actual

peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/peliculas/externas", methods=["GET"])
@requiere_admin
def get_externas():
    titulo = peliculas_validator.validar_get_externas(request.args)
    lista_omdb = peliculas_service.buscar_externas(titulo)
    return jsonify({"resultados": lista_omdb}), 200

@peliculas_bp.route("/peliculas", methods=["GET"])
@requiere_usuario
def get_peliculas():
    filtros = peliculas_validator.validar_filtros_peliculas(request.args)
    usuario = usuario_actual()
    peliculas = peliculas_service.listar_peliculas(filtros, usuario['rol'])
    return jsonify({"peliculas": peliculas}), 200

@peliculas_bp.route("/peliculas/<int:id>", methods=["GET"])
@requiere_usuario
def get_pelicula(id):
    peliculas_validator.validar_id(id)
    usuario = usuario_actual()
    pelicula = peliculas_service.obtener_pelicula_por_id(id, usuario['rol'])
    return jsonify(pelicula), 200

@peliculas_bp.route("/peliculas", methods=["POST"])
@requiere_admin
def create_pelicula():
    datos_recibidos = request.get_json(silent=True)
    datos_limpios = peliculas_validator.validar_pelicula(datos_recibidos)
    resultado = peliculas_service.crear_pelicula(datos_limpios)
    return jsonify({"id_pelicula": resultado["id"]}), 201

@peliculas_bp.route("/peliculas/<int:id>", methods=["PUT"])
@requiere_admin
def update_pelicula(id):
    peliculas_validator.validar_id(id)
    datos_recibidos = request.get_json(silent=True)
    datos_limpios = peliculas_validator.validar_pelicula(datos_recibidos)
    peliculas_service.actualizar_pelicula(id, datos_limpios)
    return "", 204

@peliculas_bp.route("/peliculas/<int:id>", methods=["DELETE"])
@requiere_admin
def delete_pelicula(id):
    peliculas_validator.validar_id(id)
    peliculas_service.eliminar_pelicula(id)
    return "", 204
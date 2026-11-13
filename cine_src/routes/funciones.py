from flask import Blueprint, jsonify, request

from security import requiere_admin, requiere_usuario
from services import funciones as servicio

funciones_bp = Blueprint("funciones", __name__)


@funciones_bp.get("/cartelera")
@requiere_usuario
def listar_cartelera():
    return jsonify(servicio.listar_cartelera(request.args)), 200


@funciones_bp.get("/funciones")
def listar_funciones():
    return jsonify(servicio.listar_funciones(request.args)), 200


@funciones_bp.get("/funciones/<int:id_funcion>")
@requiere_usuario
def buscar_funcion_por_id(id_funcion):
    return jsonify(servicio.buscar_funcion_por_id(id_funcion)), 200


@funciones_bp.post("/funciones")
@requiere_admin
def crear_funcion():
    resultado = servicio.crear_funcion(request.get_json(silent=True))
    return jsonify(resultado), 201


@funciones_bp.patch("/funciones/<int:id_funcion>")
@requiere_admin
def modificar_funcion(id_funcion):
    servicio.modificar_funcion(id_funcion, request.get_json(silent=True))
    return "", 204


@funciones_bp.delete("/funciones/<int:id_funcion>")
@requiere_admin
def eliminar_funcion(id_funcion):
    servicio.eliminar_funcion(id_funcion)
    return "", 204

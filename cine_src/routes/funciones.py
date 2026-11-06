from flask import Blueprint, jsonify, request

from security import requiere_usuario
from services import funciones as servicio

funciones_bp = Blueprint("funciones", __name__)


@funciones_bp.get("/cartelera")
@requiere_usuario
def listar_cartelera():
    return jsonify(servicio.listar_cartelera(request.args)), 200


@funciones_bp.get("/funciones")
@requiere_usuario
def listar_funciones():
    return jsonify(servicio.listar_funciones(request.args)), 200


@funciones_bp.get("/funciones/<int:id_funcion>")
@requiere_usuario
def buscar_funcion_por_id(id_funcion):
    return jsonify(servicio.buscar_funcion_por_id(id_funcion)), 200

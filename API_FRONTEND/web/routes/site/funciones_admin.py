from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

funciones_admin_bp = Blueprint("funciones_admin", __name__)


def verificar_admin():
    if session.get("rol") != "administrador":
        abort(403, description="Acceso solo para administradores")


@funciones_admin_bp.get("/gestion/funciones")
def listar_funciones_admin():
    verificar_admin()

    try:
        funciones, _ = llamar_api("GET", "/funciones")
    except HTTPException as error:
        flash(error.description)
        funciones = []

    return render_template(
        "funciones_admin.html",
        active_page="gestion",
        funciones=funciones
    )


@funciones_admin_bp.post("/gestion/funciones/crear")
def crear_funcion_admin():
    verificar_admin()

    datos = {
        "id_pelicula": request.form.get("id_pelicula", type=int),
        "id_sala": request.form.get("id_sala", type=int),
        "fecha_hora": request.form.get("fecha_hora", "").replace("T", " ") + ":00",
        "precio": request.form.get("precio", type=int)
    }

    try:
        llamar_api("POST", "/funciones", json=datos)
        flash("Función creada correctamente")
    except HTTPException as error:
        flash(error.description)

    return redirect(url_for("funciones_admin.listar_funciones_admin"))


@funciones_admin_bp.post("/gestion/funciones/<int:id_funcion>/editar")
def editar_funcion_admin(id_funcion):
    verificar_admin()

    datos = {}
    for campo in ("id_pelicula", "id_sala", "precio"):
        valor = request.form.get(campo)
        if valor is not None and valor != "":
            datos[campo] = int(valor) if valor.isdecimal() else valor

    fecha = request.form.get("fecha_hora")
    if fecha:
        datos["fecha_hora"] = fecha

    try:
        llamar_api("PATCH", f"/funciones/{id_funcion}", json=datos)
        flash("Función actualizada correctamente")
    except HTTPException as error:
        flash(error.description)

    return redirect(url_for("funciones_admin.listar_funciones_admin"))


@funciones_admin_bp.post("/gestion/funciones/<int:id_funcion>/eliminar")
def eliminar_funcion_admin(id_funcion):
    verificar_admin()

    try:
        llamar_api("DELETE", f"/funciones/{id_funcion}")
        flash("Función eliminada correctamente")
    except HTTPException as error:
        flash(error.description)

    return redirect(url_for("funciones_admin.listar_funciones_admin"))

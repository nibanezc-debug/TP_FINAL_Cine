from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException

from api_client import llamar_api

funcion_bp = Blueprint("funcion", __name__)


# Lee los filtros de la URL. Los inválidos no se mandan al backend.
def leer_filtros():
    filtros = {}
    id_local = request.args.get("id_local", "")
    fecha = request.args.get("fecha", "")

    if id_local:
        if id_local.isdigit() and int(id_local) > 0:
            filtros["id_local"] = id_local
        else:
            flash("El cine elegido no es válido.")

    if fecha:
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            filtros["fecha"] = fecha
        except ValueError:
            flash("La fecha debe tener formato AAAA-MM-DD.")

    return filtros


# GET /api/cartelera requiere sesión. Devuelve None si hay que iniciar sesión.
def consultar_cartelera(filtros):
    if not session.get("usuario_id"):
        return None

    try:
        peliculas, _ = llamar_api("GET", "/cartelera", params=filtros)
    except HTTPException as error:
        if error.code == 401:
            # la sesión del backend venció
            session.clear()
            return None
        raise

    return peliculas or []


@funcion_bp.route("/cartelera/peliculas/<int:id_pelicula>", methods=["GET", "POST"])
def get_funciones(id_pelicula):
    if request.method == "POST":
        id_funcion = request.form.get("id_funcion")
        if id_funcion and id_funcion.isdigit():
            return redirect(url_for("butacas.vista_butacas", id_funcion=int(id_funcion)))

    funciones, _ = llamar_api(
        "GET",
        f"/funciones?id_pelicula={id_pelicula}",
        con_sesion=False
    )
    pelicula, _ = llamar_api(
        "GET",
        f"/peliculas/{id_pelicula}",
        con_sesion=False,
    )

    return render_template(
        "detalle_pelicula.html",
        pelicula=pelicula or {},
        funciones=funciones or [],
        active_page="cartelera",
    )
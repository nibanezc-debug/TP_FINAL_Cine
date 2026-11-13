from flask import Blueprint, redirect, render_template, request, url_for
from api_client import llamar_api

funcion_bp = Blueprint("funcion", __name__)


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
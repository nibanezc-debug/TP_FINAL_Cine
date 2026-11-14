from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

funcion_bp = Blueprint("funcion", __name__)

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

# Cualquier usuario, logueado o no, puede ver la cartelera
def consultar_cartelera(filtros):
    try:
        # con_sesion=False asegura que no exija estar logueado
        peliculas, _ = llamar_api("GET", "/cartelera", params=filtros, con_sesion=False)
    except HTTPException as error:
        # Si el backend sigue exigiendo sesión por error de otro compañero, atajamos la caída
        if error.code == 401:
            return []
        raise

    return peliculas or []


@funcion_bp.route("/cartelera/peliculas/<int:id_pelicula>", methods=["GET", "POST"])
def get_funciones(id_pelicula):
    filtros = leer_filtros() 
    
    if request.method == "POST":
        id_funcion = request.form.get("id_funcion", "")
        if id_funcion.isdigit():
            # Acá el usuario eligió horario. Si no está logueado, podríamos frenarlo acá
            if not session.get("usuario_id"):
                flash("Por favor, iniciá sesión para comprar butacas.")
                return redirect(url_for("vistas.cartelera"))
            
            return redirect(url_for("butacas.vista_butacas", id=int(id_funcion)))
            
        flash("Elegí una función para continuar.")
        return redirect(url_for("funcion.get_funciones", id_pelicula=id_pelicula, **filtros))

    peliculas = consultar_cartelera(filtros)

    pelicula = None
    for p in peliculas:
        if p["id_pelicula"] == id_pelicula:
            pelicula = p

    if pelicula is None:
        try:
            # con_sesion=False para que el invitado pueda ver la info de la peli
            pelicula, _ = llamar_api("GET", f"/peliculas/{id_pelicula}", con_sesion=False)
            pelicula["funciones"] = []
        except HTTPException:
            flash("No se pudo encontrar la película.")
            return redirect(url_for("vistas.cartelera", **filtros))

    funciones = []
    if pelicula.get("funciones"):
        try:
            listado, _ = llamar_api("GET", "/funciones", params=dict(filtros, id_pelicula=id_pelicula), con_sesion=False)
            ofrecidas = [f["id"] for f in pelicula["funciones"]]
            funciones = [f for f in listado if f["id"] in ofrecidas]
        except Exception:
            pass

    return render_template(
        "detalle_pelicula.html",
        pelicula=pelicula,
        funciones=funciones,
        filtros=filtros,
        active_page="cartelera",
    )
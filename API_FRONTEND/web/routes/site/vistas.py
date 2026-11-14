from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from api_client import llamar_api
from werkzeug.exceptions import HTTPException
from web.routes.site.funcion import leer_filtros, consultar_cartelera

vistas_bp = Blueprint("vistas", __name__)

@vistas_bp.route("/cartelera")
def cartelera():
    filtros = leer_filtros()
    peliculas = consultar_cartelera(filtros)
    locales, _ = llamar_api("GET", "/locales", con_sesion=False)

    return render_template(
        "cartelera.html",
        active_page="cartelera",
        peliculas=peliculas or [],
        locales=locales or [],
        filtros=filtros
    )

@vistas_bp.route("/gestion")
def gestion():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))
    
    # 1. Obtener las películas para llenar la tabla del administrador
    try:
        datos, _ = llamar_api("GET", "/peliculas")
        peliculas = (datos or {}).get("peliculas", [])
    except Exception:
        peliculas = []
    
    # 2. Manejar la búsqueda externa en OMDb
    titulo_busqueda = request.args.get("titulo_omdb")
    externas = []
    if titulo_busqueda:
        try:
            datos_ext, _ = llamar_api("GET", f"/peliculas/externas?titulo={titulo_busqueda}")
            externas = datos_ext.get("resultados", [])
        except HTTPException:
            flash("Error al buscar en OMDb.")

    return render_template("gestion.html", active_page="gestion", peliculas=peliculas, externas=externas)

@vistas_bp.route("/gestion/pelicula/guardar", methods=["POST"])
def guardar_pelicula():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))
    
    pelicula_id = request.form.get("id_pelicula")
    payload = {
        "titulo": request.form.get("title"),
        "genero": request.form.get("genre"),
        "duracion_minutos": int(request.form.get("duration", 0)),
        "clasificacion": request.form.get("rating"),
        "activa": request.form.get("status") != "Inactiva",
        "sinopsis": request.form.get("sinopsis", ""),
        "poster_url": request.form.get("poster_url", "")
    }

    try:
        if pelicula_id:
            llamar_api("PUT", f"/peliculas/{pelicula_id}", json=payload)
            flash("Película actualizada con éxito.")
        else:
            llamar_api("POST", "/peliculas", json=payload)
            flash("Película creada con éxito.")
    except HTTPException as e:
        flash(f"Error al guardar: {e.description}")

    return redirect(url_for("vistas.gestion"))

@vistas_bp.route("/gestion/pelicula/eliminar/<int:id_pelicula>", methods=["POST"])
def eliminar_pelicula(id_pelicula):
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))
    
    try:
        llamar_api("DELETE", f"/peliculas/{id_pelicula}", cookies=session.get("api_cookies"))
        flash("Película dada de baja.")
    except HTTPException as e:
        flash(f"Error al eliminar: {e.description}")
        
    return redirect(url_for("vistas.gestion"))

@vistas_bp.route("/checkout")
def checkout():
    return render_template("checkout.html", active_page="checkout")

@vistas_bp.route("/comprobante")
def comprobante():
    return render_template("comprobante.html", active_page="comprobante")

@vistas_bp.route("/entradas")
def entradas():
    if not session.get("usuario_id"):
        return redirect(url_for("vistas.cartelera"))
    return render_template("mis_entradas.html", active_page="entradas")

@vistas_bp.route("/dashboard")
def dashboard():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))
    return render_template("dashboard.html", active_page="dashboard")
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
    
    # Obtener las películas para llenar la tabla del administrador
    try:
        datos, _ = llamar_api("GET", "/peliculas")
        peliculas = (datos or {}).get("peliculas", [])
    except Exception:
        peliculas = []
    
    # Manejar la búsqueda externa en OMDb
    titulo_busqueda = request.args.get("titulo_omdb")
    externas = []
    if titulo_busqueda:
        try:
            datos_ext, _ = llamar_api("GET", f"/peliculas/externas?titulo={titulo_busqueda}")
            externas = datos_ext.get("resultados", [])
        except HTTPException as error:
            flash(f"Error al buscar en OMDb : {error.description}")

    return render_template("gestion.html", active_page="gestion", peliculas=peliculas, externas=externas)

def _normalizar_fecha_form(valor):
    texto = (valor or "").strip()
    if not texto:
        return None
    if len(texto) == 16 and "T" in texto:
        return texto.replace("T", " ") + ":00"
    return texto


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
        "poster_url": request.form.get("poster_url", ""),
        "disponible_desde": _normalizar_fecha_form(request.form.get("disponible_desde")),
        "disponible_hasta": _normalizar_fecha_form(request.form.get("disponible_hasta")),
    }

    try:
        if pelicula_id:
            llamar_api("PUT", f"/peliculas/{pelicula_id}", json=payload)
            flash("Película actualizada con éxito.", "exito")
        else:
            llamar_api("POST", "/peliculas", json=payload)
            flash("Película creada con éxito.", "exito")
    except HTTPException as e:
        flash(f"Error al guardar: {e.description}")

    return redirect(url_for("vistas.gestion"))

@vistas_bp.route("/gestion/pelicula/eliminar/<int:id_pelicula>", methods=["POST"])
def eliminar_pelicula(id_pelicula):
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))

    try:
        llamar_api("DELETE", f"/peliculas/{id_pelicula}")
        flash("Película dada de baja.", "exito")
    except HTTPException as e:
        flash(f"Error al eliminar: {e.description}")

    return redirect(url_for("vistas.gestion"))

@vistas_bp.route("/dashboard")
def dashboard():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))

    ocupacion = []
    ocupacion_pelicula = []
    ventas_genero = []
    franjas_horarias = []
    cancelaciones = []
    funciones = []

    try:
        ocupacion, _ = llamar_api(
            "GET", "/entradas/estadisticas/ocupacion?agrupar=funcion"
        )
        ocupacion_pelicula, _ = llamar_api(
            "GET", "/entradas/estadisticas/ocupacion?agrupar=pelicula"
        )
        ventas_genero, _ = llamar_api(
            "GET", "/entradas/estadisticas/ventas-genero"
        )
        franjas_horarias, _ = llamar_api(
            "GET", "/entradas/estadisticas/franjas-horarias"
        )
        cancelaciones, _ = llamar_api(
            "GET", "/entradas/estadisticas/cancelaciones"
        )
        funciones, _ = llamar_api(
            "GET", "/funciones"
        )
    except HTTPException:
        flash("No se pudieron cargar las estadísticas")
        ocupacion = []
        ocupacion_pelicula = []
        ventas_genero = []
        franjas_horarias = []
        cancelaciones = []
        funciones = []

    total_entradas = 0
    importe_entradas = 0.0
    for genero in ventas_genero:
        total_entradas += int(genero.get("entradas") or 0)
        importe_entradas += float(genero.get("recaudado") or 0)
    importe_entradas = round(importe_entradas, 2)

    total_vendidas = 0
    capacidad_total = 0
    for funcion in ocupacion:
        total_vendidas += int(funcion.get("vendidas") or 0)
        capacidad_total += int(funcion.get("capacidad") or 0)

    porcentaje_ocupacion = 0
    if capacidad_total > 0:
        porcentaje_ocupacion = round(total_vendidas * 100 / capacidad_total, 1)

    total_cancelaciones = 0
    for fila in cancelaciones:
        total_cancelaciones += int(fila.get("cancelaciones") or 0)

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        ocupacion=ocupacion,
        ocupacion_pelicula=ocupacion_pelicula,
        ventas_genero=ventas_genero,
        franjas_horarias=franjas_horarias,
        cancelaciones=cancelaciones,
        funciones=funciones,
        total_entradas=total_entradas,
        importe_entradas=importe_entradas,
        porcentaje_ocupacion=porcentaje_ocupacion,
        total_cancelaciones=total_cancelaciones,
    )


@vistas_bp.route("/gestion/qr", methods=["GET", "POST"])
def validar_qr():

    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))

    if request.method == "POST":

        codigo_qr = request.form.get("codigo_qr", "").strip()
        id_funcion = request.form.get("id_funcion", type=int)

        datos = {
            "codigo_qr": codigo_qr,
            "id_funcion": id_funcion
        }

        try:
            resultado, _ = llamar_api(
                "POST",
                "/entradas/validar",
                json=datos
            )

            if resultado.get("valida"):
                flash("Entrada válida. Ingreso autorizado.", "exito")

        except HTTPException as error:
            flash("No se pudo validar la entrada: " + error.description)

        return redirect(url_for("vistas.validar_qr"))

    return render_template(
        "qr.html",
        active_page="qr"
    )

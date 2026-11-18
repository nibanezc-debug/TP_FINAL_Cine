from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

usuarios_bp = Blueprint("usuarios_admin", __name__)


@usuarios_bp.route("/gestion/usuarios")
def listar_usuarios():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))

    try:
        datos, _ = llamar_api("GET", "/usuarios")
        usuarios = datos if isinstance(datos, list) else datos.get("usuarios", [])
    except HTTPException as e:
        flash(f"Error al cargar usuarios: {e.description}")
        usuarios = []

    return render_template("usuarios.html", active_page="usuarios", usuarios=usuarios)


@usuarios_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    id_usuario = session.get("usuario_id")
    if not id_usuario:
        flash("Iniciá sesión para ver tu perfil.")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        try:
            actualizado, _ = llamar_api(
                "PUT",
                f"/usuarios/{id_usuario}",
                json={"nombre": nombre, "email": email},
            )
            session["email"] = (actualizado or {}).get("email", email)
            flash("Datos del perfil actualizados correctamente.", "exito")
        except HTTPException as e:
            flash(f"No se pudo actualizar el perfil: {e.description}")
        return redirect(url_for("usuarios_admin.perfil"))

    try:
        usuario, _ = llamar_api("GET", f"/usuarios/{id_usuario}")
    except HTTPException as e:
        flash(f"No se pudo cargar el perfil: {e.description}")
        return redirect(url_for("vistas.cartelera"))

    peliculas_vistas = []
    consumos_historial = []
    total_consumos = 0

    if session.get("rol") == "cliente":
        try:
            entradas_raw, _ = llamar_api("GET", "/entradas/mias")
            entradas = (
                entradas_raw
                if isinstance(entradas_raw, list)
                else (entradas_raw or {}).get("entradas", [])
            )
        except HTTPException:
            entradas = []

        funciones_cache = {}
        vistas_por_funcion = {}
        reservas_info = {}
        ahora = datetime.now()

        for e in entradas:
            id_funcion = e.get("id_funcion")
            if id_funcion not in funciones_cache:
                try:
                    funciones_cache[id_funcion], _ = llamar_api("GET", f"/funciones/{id_funcion}")
                except HTTPException:
                    funciones_cache[id_funcion] = {}

            funcion = funciones_cache[id_funcion] or {}
            estado = e.get("estado")
            fecha_str = e.get("fecha_hora_funcion") or funcion.get("fecha_hora") or ""

            es_pasada = False
            if fecha_str:
                try:
                    es_pasada = datetime.fromisoformat(fecha_str) <= ahora
                except ValueError:
                    es_pasada = False

            # Se considera vista si la entrada fue usada o la función ya pasó sin cancelarse
            if estado == "usada" or (estado == "activa" and es_pasada):
                if id_funcion not in vistas_por_funcion:
                    vistas_por_funcion[id_funcion] = {
                        "titulo": funcion.get("titulo", f"Función #{id_funcion}"),
                        "poster_url": funcion.get("poster_url", ""),
                        "local": funcion.get("local", ""),
                        "sala": funcion.get("sala", ""),
                        "clasificacion": funcion.get("clasificacion", ""),
                        "fecha_hora": fecha_str,
                        "cantidad_entradas": 0,
                    }
                vistas_por_funcion[id_funcion]["cantidad_entradas"] += 1

            id_reserva = e.get("id_reserva")
            if id_reserva and id_reserva not in reservas_info:
                reservas_info[id_reserva] = {
                    "pelicula": funcion.get("titulo", f"Función #{id_funcion}"),
                    "fecha": fecha_str[:10] if fecha_str else "-",
                }

        peliculas_vistas = sorted(
            vistas_por_funcion.values(),
            key=lambda x: x["fecha_hora"],
            reverse=True,
        )

        for id_reserva, info in reservas_info.items():
            try:
                consumos, _ = llamar_api("GET", f"/reservas/{id_reserva}/consumos")
            except HTTPException:
                consumos = []

            for c in consumos or []:
                subtotal = c.get("subtotal", 0)
                total_consumos += subtotal
                consumos_historial.append({
                    "id_reserva": id_reserva,
                    "pelicula": info["pelicula"],
                    "fecha": info["fecha"],
                    "nombre": c.get("nombre", "Servicio"),
                    "cantidad": c.get("cantidad", 1),
                    "precio_unitario": c.get("precio_unitario", 0),
                    "subtotal": subtotal,
                })

    return render_template(
        "perfil.html",
        active_page="perfil",
        usuario=usuario or {},
        peliculas_vistas=peliculas_vistas,
        consumos_historial=consumos_historial,
        total_consumos=total_consumos,
    )
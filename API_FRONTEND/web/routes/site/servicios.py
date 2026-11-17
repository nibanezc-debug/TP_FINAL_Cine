"""Backoffice de servicios, integrado con el login y api_client del grupo."""
import hmac
import secrets

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

servicios_web_bp = Blueprint("servicios_web", __name__)


@servicios_web_bp.context_processor
def inyectar_csrf():
    """Provee tokens CSRF solamente a los templates de este Blueprint."""
    def csrf_token():
        if "csrf_servicios" not in session:
            session["csrf_servicios"] = secrets.token_urlsafe(32)
        return session["csrf_servicios"]
    return {"csrf_token": csrf_token}


def solo_administrador():
    if not session.get("usuario_id"):
        return redirect(url_for("auth.login"))
    if session.get("rol") != "administrador":
        abort(403)
    return None


def verificar_csrf():
    enviado = request.form.get("csrf_token", "")
    esperado = session.get("csrf_servicios", "")
    if not esperado or not hmac.compare_digest(enviado, esperado):
        abort(400, description="Formulario inválido o expirado")


@servicios_web_bp.get("/gestion/servicios")
def mostrar_servicios():
    redireccion = solo_administrador()
    if redireccion is not None:
        return redireccion
    try:
        servicios, _ = llamar_api("GET", "/servicios")
    except HTTPException as error:
        if error.code == 401:
            session.clear()
            return redirect(url_for("auth.login"))
        flash(f"No se pudieron cargar los servicios: {error.description}", "error")
        servicios = []
    return render_template("gestion_servicios.html", servicios=servicios or [], active_page="servicios")


@servicios_web_bp.post("/gestion/servicios/nuevo")
def crear_servicio():
    redireccion = solo_administrador()
    if redireccion is not None:
        return redireccion
    verificar_csrf()
    try:
        nombre = request.form.get("nombre", "").strip()
        precio = int(request.form.get("precio", ""))
        llamar_api("POST", "/servicios", json={"nombre": nombre, "precio": precio})
        flash("Servicio creado correctamente", "exito")
    except ValueError:
        flash("El precio debe ser un número entero", "error")
    except HTTPException as error:
        flash(f"No se pudo crear el servicio: {error.description}", "error")
    return redirect(url_for("servicios_web.mostrar_servicios"))


@servicios_web_bp.post("/gestion/servicios/<int:identificador>/editar")
def editar_servicio(identificador):
    redireccion = solo_administrador()
    if redireccion is not None:
        return redireccion
    verificar_csrf()
    try:
        nombre = request.form.get("nombre", "").strip()
        precio = int(request.form.get("precio", ""))
        llamar_api("PUT", f"/servicios/{identificador}", json={"nombre": nombre, "precio": precio})
        flash("Servicio actualizado correctamente", "exito")
    except ValueError:
        flash("El precio debe ser un número entero", "error")
    except HTTPException as error:
        flash(f"No se pudo actualizar el servicio: {error.description}", "error")
    return redirect(url_for("servicios_web.mostrar_servicios"))


@servicios_web_bp.post("/gestion/servicios/<int:identificador>/baja")
def bajar_servicio(identificador):
    redireccion = solo_administrador()
    if redireccion is not None:
        return redireccion
    verificar_csrf()
    try:
        llamar_api("DELETE", f"/servicios/{identificador}")
        flash("Servicio dado de baja correctamente", "exito")
    except HTTPException as error:
        flash(f"No se pudo dar de baja el servicio: {error.description}", "error")
    return redirect(url_for("servicios_web.mostrar_servicios"))

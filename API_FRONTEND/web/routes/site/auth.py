from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

auth_bp = Blueprint("auth", __name__)


def destino_seguro(destino):
    # Solo rutas internas como "/entradas/7/cancelar"; nada de "//otro.com", "http://..." ni "\".
    # Los caracteres de control se rechazan porque el navegador los borra ("/\t/otro.com" -> "//otro.com").
    if not destino or not destino.startswith("/") or destino.startswith("//") or "\\" in destino:
        return None
    if any(ord(c) < 32 or ord(c) == 127 for c in destino):
        return None
    return destino


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", active_page="login", next=destino_seguro(request.args.get("next")))

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    destino = destino_seguro(request.form.get("next"))

    try:
        datos, resp = llamar_api("POST", "/auth/login", json={"email": email, "password": password})
    except HTTPException as e:
        flash(f"Error al iniciar sesión: {e.description}")
        return redirect(url_for("auth.login", next=destino))

    datos = datos or {}
    usuario = datos.get("usuario", datos)
    
    id_usuario = usuario.get("id_usuario") or usuario.get("id")
    
    if not id_usuario:
        flash("Respuesta inesperada del backend.")
        return redirect(url_for("auth.login"))

    session["usuario_id"] = id_usuario
    session["email"] = usuario.get("email", email)
    session["rol"] = usuario.get("rol", "cliente")
    session["api_cookies"] = resp.cookies.get_dict()

    # Si venía de un enlace (por ejemplo, cancelar desde el correo), vuelve ahí
    if destino:
        return redirect(destino)
    if session["rol"] == "administrador":
        return redirect(url_for("vistas.gestion"))
    return redirect(url_for("vistas.cartelera"))

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html", active_page="registro")
    
    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        llamar_api("POST", "/auth/register", json={"nombre": nombre, "email": email, "password": password})
        flash("Cuenta creada con éxito. Ya podés iniciar sesión.", "exito")
        return redirect(url_for("auth.login"))
    except HTTPException as e:
        flash(f"Error al registrarse: {e.description}")
        return redirect(url_for("auth.registro"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("vistas.cartelera"))
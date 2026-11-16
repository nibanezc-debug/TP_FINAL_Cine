from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", active_page="login")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        try:
            datos, resp = llamar_api("POST", "/usuarios/login", json={"email": email, "password": password})
        except HTTPException as e:
            if e.code == 404:
                datos, resp = llamar_api("POST", "/auth/login", json={"email": email, "password": password})
            else:
                raise e
    except HTTPException as e:
        flash(f"Error al iniciar sesión: {e.description}")
        return redirect(url_for("auth.login"))

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
        flash("Cuenta creada con éxito. Ya podés iniciar sesión.")
        return redirect(url_for("auth.login"))
    except HTTPException as e:
        flash(f"Error al registrarse: {e.description}")
        return redirect(url_for("auth.registro"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("vistas.cartelera"))
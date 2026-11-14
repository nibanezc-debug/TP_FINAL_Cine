from flask import Blueprint, render_template, session, redirect, url_for, flash
from werkzeug.exceptions import HTTPException
from api_client import llamar_api

usuarios_bp = Blueprint("usuarios_admin", __name__)

@usuarios_bp.route("/gestion/usuarios")
def listar_usuarios():
    if session.get("rol") != "administrador":
        return redirect(url_for("vistas.cartelera"))
    
    try:
        datos, _ = llamar_api("GET", "/usuarios")
        # Dependiendo de cómo lo devuelva tu backend, extraemos la lista
        usuarios = datos if isinstance(datos, list) else datos.get("usuarios", [])
    except HTTPException as e:
        flash(f"Error al cargar usuarios: {e.description}")
        usuarios = []

    return render_template("usuarios.html", active_page="usuarios", usuarios=usuarios)
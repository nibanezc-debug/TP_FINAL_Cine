import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException
from web.routes.site.butacas import butacas_bp
from web.routes.site.funcion import funcion_bp
from web.routes.site.vistas import vistas_bp

from api_client import llamar_api, CODIGOS_ERROR

def mostrar_error(e):
    return render_template("error.html", codigo=e.code, mensaje=e.description), e.code

def crear_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_secreta_frontend")
    if not app.secret_key:
        raise RuntimeError("Es necesario configurar FLASK_SECRET_KEY")

    app.config["API_URL"] = os.getenv("API_URL", "http://127.0.0.1:5000/api")
    app.config["SESSION_COOKIE_NAME"] = "cine_front"

    for codigo in CODIGOS_ERROR:
        app.register_error_handler(codigo, mostrar_error)
        
    app.register_blueprint(vistas_bp)
    app.register_blueprint(butacas_bp)
    app.register_blueprint(funcion_bp)

    @app.route("/")
    def index():
        return redirect(url_for("vistas.cartelera"))

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        try:
            try:
                datos, resp = llamar_api(
                    "POST", "/usuarios/login", json={"email": email, "password": password}
                )
            except HTTPException as e:
                if e.code == 404:
                    datos, resp = llamar_api(
                        "POST", "/auth/login", json={"email": email, "password": password}
                    )
                else:
                    raise e
        except HTTPException as e:
            flash(e.description)
            return redirect(url_for("vistas.cartelera"))

        datos = datos or {}
        usuario = datos.get("usuario", datos)
        
        id_usuario = usuario.get("id_usuario") or usuario.get("id")
        
        if not id_usuario:
            flash("Respuesta inesperada del backend.")
            return redirect(url_for("vistas.cartelera"))

        session["usuario_id"] = id_usuario
        session["email"] = usuario.get("email", email)
        session["rol"] = usuario.get("rol", "cliente")
        session["api_cookies"] = resp.cookies.get_dict()

        if session["rol"] == "administrador":
            return redirect(url_for("vistas.gestion"))
        return redirect(url_for("vistas.cartelera"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("vistas.cartelera"))

    return app

if __name__ == "__main__":
    app_front = crear_app()
    app_front.run(host="127.0.0.1", port=5001, debug=True)
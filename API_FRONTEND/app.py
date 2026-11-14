import os
from flask import Flask, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException
from api_client import CODIGOS_ERROR

# Importamos todos los blueprints
from web.routes.site.butacas import butacas_bp
from web.routes.site.funcion import funcion_bp
from web.routes.site.funciones_admin import funciones_admin_bp
from web.routes.site.vistas import vistas_bp 
from web.routes.site.auth import auth_bp             
from web.routes.site.usuarios import usuarios_bp    

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

    @app.route("/")
    def index():
        return redirect(url_for("vistas.cartelera"))
    
    # Registramos todos los Blueprints
    app.register_blueprint(butacas_bp)
    app.register_blueprint(funcion_bp)
    app.register_blueprint(funciones_admin_bp)
    app.register_blueprint(vistas_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)

    return app

if __name__ == "__main__":
    app_front = crear_app()
    app_front.run(host="127.0.0.1", port=5001, debug=True)
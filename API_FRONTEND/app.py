import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException

from api_client import llamar_api, CODIGOS_ERROR


def mostrar_error(e):
    return render_template("error.html", codigo=e.code, mensaje=e.description), e.code


def crear_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    if not app.secret_key:
        raise RuntimeError("Es necesario configurar FLASK_SECRET_KEY")

    app.config["API_URL"] = os.getenv("API_URL", "http://127.0.0.1:5000/api")
    # Las cookies no distinguen puertos: sin esto, front y back se pisan la cookie "session".
    app.config["SESSION_COOKIE_NAME"] = "cine_front"

    for codigo in CODIGOS_ERROR:
        app.register_error_handler(codigo, mostrar_error)

    @app.route("/")
    def index():
        return redirect(url_for("cartelera"))

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        try:
            # SUPUESTO: la ruta es /api/usuarios/login. Confirmarlo en routes/usuarios.py
            datos, resp = llamar_api(
                "POST", "/usuarios/login", json={"email": email, "password": password}
            )
        except HTTPException as e:
            flash(e.description)
            return redirect(url_for("cartelera"))

        datos = datos or {}
        usuario = datos.get("usuario", datos)
        if "id" not in usuario:
            flash("Respuesta inesperada del backend.")
            return redirect(url_for("cartelera"))

        session["usuario_id"] = usuario["id"]
        session["email"] = usuario.get("email", email)
        session["rol"] = usuario.get("rol", "cliente")
        session["api_cookies"] = resp.cookies.get_dict()

        if session["rol"] == "administrador":
            return redirect(url_for("gestion"))
        return redirect(url_for("cartelera"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("cartelera"))

    @app.route("/cartelera")
    def cartelera():
        datos, _ = llamar_api("GET", "/peliculas", con_sesion=False)
        peliculas = (datos or {}).get("peliculas", [])
        return render_template("cartelera.html", active_page="cartelera", peliculas=peliculas)
    
    @app.route("/butacas")
    def butacas():
        return render_template("butacas.html", active_page="butacas")

    @app.route("/checkout")
    def checkout():
        return render_template("checkout.html", active_page="checkout")

    @app.route("/comprobante")
    def comprobante():
        return render_template("comprobante.html", active_page="comprobante")

    @app.route("/entradas")
    def entradas():
        if not session.get("usuario_id"):
            return redirect(url_for("cartelera"))
        return render_template("mis_entradas.html", active_page="entradas")

    @app.route("/gestion")
    def gestion():
        if session.get("rol") != "administrador":
            return redirect(url_for("cartelera"))
        return render_template("gestion.html", active_page="gestion")

    @app.route("/dashboard")
    def dashboard():
        if session.get("rol") != "administrador":
            return redirect(url_for("cartelera"))
        return render_template("dashboard.html", active_page="dashboard")

    return app


if __name__ == "__main__":
    app_front = crear_app()
    app_front.run(host="127.0.0.1", port=5001, debug=True)
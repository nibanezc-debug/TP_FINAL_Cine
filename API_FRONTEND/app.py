import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.exceptions import HTTPException
from web.routes.site.butacas import butacas_bp
from web.routes.site.funcion import funcion_bp
from web.routes.site.funciones_admin import funciones_admin_bp
from api_client import llamar_api, CODIGOS_ERROR
from web.routes.site.funcion import leer_filtros, consultar_cartelera


def mostrar_error(e):
    return render_template("error.html", codigo=e.code, mensaje=e.description), e.code


def crear_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_secreta_frontend")
    if not app.secret_key:
        raise RuntimeError("Es necesario configurar FLASK_SECRET_KEY")

    app.config["API_URL"] = os.getenv("API_URL", "http://127.0.0.1:5000/api")
    # Las cookies no distinguen puertos, sin esto, front y back se pisan la cookie "session"
    app.config["SESSION_COOKIE_NAME"] = "cine_front"

    for codigo in CODIGOS_ERROR:
        app.register_error_handler(codigo, mostrar_error)

    @app.route("/")
    def index():
        return redirect(url_for("cartelera"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return """
            <form method="POST" action="/login">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Entrar</button>
            </form>
            """

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        try:
<<<<<<< HEAD
            # (usuarios/login)
            try:
                datos, resp = llamar_api(
                    "POST", "/usuarios/login", json={"email": email, "password": password}
                )
            except HTTPException as e:
                # 2. Si no la encuentra (404), intentamos la alternativa (auth/login)
                if e.code == 404:
                    datos, resp = llamar_api(
                        "POST", "/auth/login", json={"email": email, "password": password}
                    )
                else:
                    raise e
=======
            datos, resp = llamar_api(
                "POST", "/usuarios/login", json={"email": email, "password": password}
            )
>>>>>>> feature/butacas_rutas
        except HTTPException as e:
            flash(e.description)
            return redirect(url_for("login"))

        datos = datos or {}
        usuario = datos.get("usuario", datos)
        
        id_usuario = usuario.get("id_usuario") or usuario.get("id")
        
        if not id_usuario:
            flash("Respuesta inesperada del backend.")
            return redirect(url_for("login"))

        session["usuario_id"] = id_usuario
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
        filtros = leer_filtros()
        peliculas = consultar_cartelera(filtros)
        locales, _ = llamar_api("GET", "/locales", con_sesion=False)

        return render_template(
            "cartelera.html",
            active_page="cartelera",
            peliculas=peliculas or [],
            locales=locales or [],
            filtros=filtros,
            requiere_login=peliculas is None,
        )
    
    app.register_blueprint(butacas_bp)
    app.register_blueprint(funcion_bp)
    app.register_blueprint(funciones_admin_bp)

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


@app.route("/registro")
def registro():
    return render_template("registro.html", active_page="registro")


@app.route("/login")
def login():
    return render_template("login.html", active_page="login")


@app.route("/perfil")
def perfil():
    return render_template("perfil.html", usuario={}, active_page="perfil")


@app.route("/usuarios")
def listar_usuarios():
    return render_template("usuarios.html", usuarios=[], active_page="usuarios")

if __name__ == "__main__":
    app_front = crear_app()
    app_front.run(host="127.0.0.1", port=5001, debug=True)

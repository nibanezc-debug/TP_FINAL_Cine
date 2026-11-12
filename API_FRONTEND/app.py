from flask import Flask, render_template, redirect, url_for
# import requests  # Descomentar al conectar con el backend en http://localhost:5000

app = Flask(__name__)
API_URL = "http://localhost:5000"


@app.route("/")
def index():
    return redirect(url_for("cartelera"))


@app.route("/cartelera")
def cartelera():
    # Ejemplo de conexión futura:
    # resp = requests.get(f"{API_URL}/api/cartelera")
    # peliculas = resp.json() if resp.status_code == 200 else []
    return render_template("cartelera.html", active_page="cartelera")


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
    return render_template("mis_entradas.html", active_page="entradas")


@app.route("/gestion")
def gestion():
    return render_template("gestion.html", active_page="gestion")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


if __name__ == "__main__":
    app.run(port=5001, debug=True)

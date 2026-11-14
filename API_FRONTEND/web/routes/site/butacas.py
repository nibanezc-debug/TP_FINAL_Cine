from flask import Blueprint, redirect, render_template, request, session, url_for
from api_client import llamar_api

butacas_bp = Blueprint("butacas", __name__)

TEMPLATES_POR_CAPACIDAD = {
    120: "butacas_120.html",
    250: "butacas_250.html",
    450: "butacas_450.html",
}


@butacas_bp.route("/cartelera/funcion/<int:id>/butacas", methods=["GET"])
def vista_butacas(id):
    # llamar_api devuelve la tupla (datos, resp); si hay error en el backend hace abort() solo
    butacas, _ = llamar_api("GET", f"/funciones/{id}/butacas", con_sesion=False)
    funcion, _ = llamar_api("GET", f"/funciones/{id}")

    butacas = butacas or []
    funcion = funcion or {}

    template_elegido = TEMPLATES_POR_CAPACIDAD.get(len(butacas))

    return render_template(
        template_elegido,
        butacas=butacas,
        funcion=funcion,
        active_page="butacas",
    )


@butacas_bp.route("/funcion/<int:id_funcion>/butacas", methods=["POST"])
def seleccionar_butacas(id_funcion):
    ids_raw = request.form.get("butacas_ids", "")
    labels = request.form.get("butacas_labels", "")

    butacas_ids = [int(x) for x in ids_raw.split(",") if x.isdigit()]
    if not butacas_ids:
        return redirect(url_for("butacas.vista_butacas", id=id_funcion))

    session["carrito"] = {
        "id_funcion": id_funcion,
        "butacas_ids": butacas_ids,
        "butacas_labels": labels,
    }
    return redirect(url_for("checkout.vista_checkout"))  # Ajustar al nombre de tu blueprint de checkout
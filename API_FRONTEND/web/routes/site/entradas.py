import base64

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from api_client import llamar_api

checkout_bp = Blueprint("checkout", __name__)
comprobante_bp = Blueprint("comprobante", __name__)
entradas_bp = Blueprint("entradas", __name__)

@checkout_bp.route("/checkout", methods=["GET", "POST"])
def vista_checkout():
    if request.method == "POST":
        return _confirmar_compra()

    carrito = session.get("carrito")
    if not carrito:
        return redirect(url_for("cartelera"))

    funcion, _ = llamar_api("GET", f"/funciones/{carrito['id_funcion']}", con_sesion=False)
    funcion = funcion or {}
    cantidad = len(carrito["butacas_ids"])

    return render_template(
        "checkout.html",
        active_page="checkout",
        carrito=carrito,
        funcion=funcion,
        cantidad=cantidad,
        total=funcion.get("precio", 0) * cantidad,
    )


def _confirmar_compra():
    carrito = session.get("carrito")
    if not carrito:
        return redirect(url_for("cartelera"))

    if not session.get("usuario_id"):
        flash("Iniciá sesión para finalizar la compra.")
        return redirect(url_for("cartelera"))

    datos, _ = llamar_api(
        "POST",
        "/entradas",
        json={"id_funcion": carrito["id_funcion"], "butacas": carrito["butacas_ids"]},
    )

    session["compra"] = {
        "id_reserva": datos.get("id_reserva"),
        "ids_entradas": [e["id"] for e in datos.get("entradas", [])],
    }
    session.pop("carrito", None)
    return redirect(url_for("comprobante.vista_comprobante"))


@comprobante_bp.route("/comprobante")
def vista_comprobante():
    compra = session.get("compra")
    if not compra:
        return redirect(url_for("entradas.vista_entradas"))

    entradas = []
    funcion = {}
    factura = None

    for id_entrada in compra["ids_entradas"]:
        entrada, _ = llamar_api("GET", f"/entradas/{id_entrada}")
        _, resp = llamar_api("GET", f"/entradas/{id_entrada}/qr")
        qr_data = "data:image/png;base64," + base64.b64encode(resp.content).decode("ascii")
        entradas.append({**entrada, "qr_data": qr_data})

        if not funcion:
            funcion, _ = llamar_api("GET", f"/funciones/{entrada['id_funcion']}", con_sesion=False)
        if factura is None:
            factura, _ = llamar_api("GET", f"/entradas/{id_entrada}/factura")

    session.pop("compra", None)
    return render_template(
        "comprobante.html",
        active_page="comprobante",
        entradas=entradas,
        funcion=funcion,
        factura=factura or {},
    )


@entradas_bp.route("/entradas")
def vista_entradas():
    if not session.get("usuario_id"):
        return redirect(url_for("cartelera"))

    datos, _ = llamar_api("GET", "/entradas/mias")
    entradas = datos if isinstance(datos, list) else (datos or {}).get("entradas", [])
    return render_template("mis_entradas.html", active_page="entradas", entradas=entradas)


@entradas_bp.route("/entradas/<int:id_entrada>/cancelar", methods=["POST"])
def cancelar_entrada(id_entrada):
    llamar_api("PATCH", f"/entradas/{id_entrada}/cancelar")
    flash("Entrada cancelada correctamente. La butaca quedó liberada.")
    return redirect(url_for("entradas.vista_entradas"))
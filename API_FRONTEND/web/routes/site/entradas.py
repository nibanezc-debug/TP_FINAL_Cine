import base64

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException

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
        flash("Todavía no elegiste butacas. Elegí una función para continuar.")
        return redirect(url_for("vistas.cartelera"))

    if not session.get("usuario_id"):
        flash("Iniciá sesión para finalizar la compra.")
        return redirect(url_for("vistas.cartelera"))

    # El detalle de la función requiere login, así que va con la sesión (api_cookies)
    funcion, _ = llamar_api("GET", f"/funciones/{carrito['id_funcion']}")
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
        flash("Todavía no elegiste butacas. Elegí una función para continuar.")
        return redirect(url_for("vistas.cartelera"))

    if not session.get("usuario_id"):
        flash("Iniciá sesión para finalizar la compra.")
        return redirect(url_for("vistas.cartelera"))

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
    # La reserva queda pendiente: primero se eligen los servicios adicionales.
    return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=datos["id_reserva"]))


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
            funcion, _ = llamar_api("GET", f"/funciones/{entrada['id_funcion']}")
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
        flash("Iniciá sesión para ver tus entradas.")
        return redirect(url_for("vistas.cartelera"))

    datos, _ = llamar_api("GET", "/entradas/mias")
    entradas = datos if isinstance(datos, list) else (datos or {}).get("entradas", [])
    return render_template("mis_entradas.html", active_page="entradas", entradas=entradas)


@entradas_bp.route("/entradas/<int:id_entrada>")
def vista_entrada(id_entrada):
    if not session.get("usuario_id"):
        flash("Iniciá sesión para ver tus entradas.")
        return redirect(url_for("vistas.cartelera"))

    # Si la entrada no existe (404) o es de otro usuario (403), llamar_api muestra la página de error
    entrada, _ = llamar_api("GET", f"/entradas/{id_entrada}")
    funcion, _ = llamar_api("GET", f"/funciones/{entrada['id_funcion']}")
    butacas, _ = llamar_api("GET", f"/funciones/{entrada['id_funcion']}/butacas")

    # El detalle trae solo el id de la butaca; buscamos su fila y columna
    butaca = f"#{entrada['id_butaca']}"
    for b in butacas or []:
        if b["id"] == entrada["id_butaca"]:
            butaca = f"{b['fila']}{b['columna']}"

    # El QR solo existe para entradas activas; el backend lo arma con el código guardado
    qr_data = None
    if entrada["estado"] == "activa":
        _, resp = llamar_api("GET", f"/entradas/{id_entrada}/qr")
        qr_data = "data:image/png;base64," + base64.b64encode(resp.content).decode("ascii")

    return render_template(
        "entrada.html",
        active_page="entradas",
        entrada=entrada,
        funcion=funcion,
        butaca=butaca,
        qr_data=qr_data,
    )


@entradas_bp.route("/entradas/<int:id_entrada>/cancelar", methods=["POST"])
def cancelar_entrada(id_entrada):
    try:
        llamar_api("PATCH", f"/entradas/{id_entrada}/cancelar")
    except HTTPException as error:
        # Sesión vencida o sin permiso: se muestran como siempre, no como error de cancelación
        if error.code in (401, 403):
            raise
        # 409: usada o cancelada, 422: venció el plazo, 404: no existe
        if error.code in (404, 409, 422):
            flash(f"No se pudo cancelar la entrada: {error.description}")
        else:
            flash("No se pudo completar la cancelación. Intentá de nuevo más tarde.")
        return redirect(url_for("entradas.vista_entradas"))

    flash("Entrada cancelada correctamente. La butaca quedó liberada.", "exito")
    return redirect(url_for("entradas.vista_entradas"))
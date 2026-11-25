import hmac
import secrets

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException

from api_client import llamar_api

consumos_web_bp = Blueprint("consumos_web", __name__)


@consumos_web_bp.context_processor
def inyectar_csrf():
    def csrf_consumos():
        if "csrf_consumos" not in session:
            session["csrf_consumos"] = secrets.token_urlsafe(32)
        return session["csrf_consumos"]
    return {"csrf_consumos": csrf_consumos}


def requerir_cliente():
    if not session.get("usuario_id"):
        flash("Iniciá sesión para gestionar tus reservas.")
        return redirect(url_for("auth.login"))
    if session.get("rol") != "cliente":
        abort(403, description="Solo los clientes pueden gestionar sus reservas")
    return None


def verificar_csrf():
    esperado = session.get("csrf_consumos", "")
    recibido = request.form.get("csrf_consumos", "")
    if not esperado or not hmac.compare_digest(recibido, esperado):
        abort(400, description="Formulario inválido o expirado")


def entradas_de_reserva(id_reserva):
    entradas, _ = llamar_api("GET", "/entradas/mias")
    datos = entradas if isinstance(entradas, list) else (entradas or {}).get("entradas", [])
    return [e for e in datos if e.get("id_reserva") == id_reserva]


@consumos_web_bp.get("/mis-reservas/consumos")
def mis_reservas():
    redireccion = requerir_cliente()
    if redireccion is not None:
        return redireccion

    entradas, _ = llamar_api("GET", "/entradas/mias")
    datos = entradas if isinstance(entradas, list) else (entradas or {}).get("entradas", [])
    reservas = {}
    for entrada in datos:
        id_reserva = entrada.get("id_reserva")
        if id_reserva is None:
            continue
        if id_reserva not in reservas:
            reservas[id_reserva] = {"id": id_reserva, "cantidad": 0}
        if entrada.get("estado") != "cancelada":
            reservas[id_reserva]["cantidad"] += 1

    return render_template("mis_reservas_consumos.html", reservas=list(reservas.values()), active_page="mis_reservas")


@consumos_web_bp.get("/checkout/servicios/<int:id_reserva>")
def mostrar_consumos(id_reserva):
    redireccion = requerir_cliente()
    if redireccion is not None:
        return redireccion

    # El backend valida la propiedad de la reserva antes de entregar el estado.
    reserva, _ = llamar_api("GET", f"/reservas/{id_reserva}")
    entradas = entradas_de_reserva(id_reserva)
    if not entradas:
        abort(404, description="No se encontraron entradas para esta reserva")

    consumos, _ = llamar_api("GET", f"/reservas/{id_reserva}/consumos")
    servicios, _ = llamar_api("GET", "/servicios")
    total_entradas = sum(e.get("precio", 0) for e in entradas if e.get("estado") != "cancelada")
    total_consumos = sum(c.get("subtotal", 0) for c in (consumos or []))

    return render_template(
        "consumos_reserva.html", active_page="mis_reservas", id_reserva=id_reserva,
        estado=reserva["estado"], servicios=servicios or [], consumos=consumos or [],
        total_entradas=total_entradas, total_consumos=total_consumos,
        total=total_entradas + total_consumos,
    )


@consumos_web_bp.post("/checkout/servicios/<int:id_reserva>/agregar")
def agregar_consumo(id_reserva):
    redireccion = requerir_cliente()
    if redireccion is not None:
        return redireccion
    verificar_csrf()

    try:
        datos = {
            "id_servicio": int(request.form.get("id_servicio", "")),
            "cantidad": int(request.form.get("cantidad", "")),
        }
        llamar_api("POST", f"/reservas/{id_reserva}/consumos", json=datos)
        flash("Servicio agregado a la reserva.", "exito")
    except ValueError:
        flash("Seleccioná un servicio y una cantidad válida.")
    except HTTPException as error:
        if error.code in (401, 403):
            raise
        flash(f"No se pudo agregar el servicio: {error.description}")
    return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=id_reserva))


@consumos_web_bp.post("/checkout/servicios/<int:id_reserva>/<int:id_consumo>/quitar")
def quitar_consumo(id_reserva, id_consumo):
    redireccion = requerir_cliente()
    if redireccion is not None:
        return redireccion
    verificar_csrf()

    try:
        llamar_api("DELETE", f"/reservas/{id_reserva}/consumos/{id_consumo}")
        flash("Servicio quitado de la reserva.", "exito")
    except HTTPException as error:
        if error.code in (401, 403):
            raise
        flash(f"No se pudo quitar el servicio: {error.description}")
    return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=id_reserva))


@consumos_web_bp.post("/checkout/servicios/<int:id_reserva>/confirmar")
def confirmar_compra(id_reserva):
    redireccion = requerir_cliente()
    if redireccion is not None:
        return redireccion
    verificar_csrf()

    try:
        reserva, _ = llamar_api("GET", f"/reservas/{id_reserva}")
        if reserva.get("estado") != "pendiente":
            flash("La reserva ya no está pendiente de pago.")
            return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=id_reserva))

        entradas = entradas_de_reserva(id_reserva)
        entrada_activa = next((e for e in entradas if e.get("estado") == "activa"), None)
        if entrada_activa is None:
            flash("La reserva no tiene entradas activas para pagar.")
            return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=id_reserva))

        # El backend envía los correos y marca la reserva como pagada.
        # Si no está configurado SMTP, comunica el error y no anuncia un pago exitoso.
        resultado, _ = llamar_api("POST", f"/entradas/{entrada_activa['id']}/pagar")
        if not resultado or resultado.get("pagada") is not True:
            abort(502, description="El backend no confirmó el pago")

        session["compra"] = {
            "id_reserva": id_reserva,
            "ids_entradas": [e["id"] for e in entradas if e.get("estado") == "activa"],
        }
        session.pop("carrito", None)
        flash("Compra confirmada. Revisá tu correo para recibir los códigos QR.", "exito")
        return redirect(url_for("comprobante.vista_comprobante"))
    except HTTPException as error:
        if error.code in (401, 403):
            raise
        flash(f"No se pudo confirmar la compra: {error.description}")
        return redirect(url_for("consumos_web.mostrar_consumos", id_reserva=id_reserva))

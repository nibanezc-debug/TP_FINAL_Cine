import html
import os
import smtplib
from email.message import EmailMessage
from errors import ApiError

def _url_cancelacion(id_entrada: int) -> str:
    # URL pública del frontend (no la del backend). En local: http://127.0.0.1:5001
    base = os.getenv('FRONTEND_URL', 'http://127.0.0.1:5001').rstrip('/')
    return f"{base}/entradas/{id_entrada}/cancelar"

def _boton(url: str, texto: str) -> str:
    return (f'<a href="{html.escape(url)}" style="display:inline-block; padding:10px 16px; background:#e50914; '
            f'color:#ffffff; text-decoration:none; border-radius:8px;">{html.escape(texto)}</a>')

def _conectar(servidor: str, puerto: int):
    if puerto == 465:
        return smtplib.SMTP_SSL(servidor, puerto, timeout=10)
    conexion = smtplib.SMTP(servidor, puerto, timeout=10)
    conexion.starttls()
    return conexion

def _configurar_mensaje(destinatario: dict, asunto: str) -> EmailMessage:
    servidor = os.getenv('SMTP_HOST')
    remitente = os.getenv('SMTP_FROM') or os.getenv('SMTP_USER')
    if not servidor or not remitente:
        raise ApiError('El envío de mails no está configurado', 503)
    mensaje = EmailMessage()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario['email']
    mensaje['Subject'] = asunto
    return mensaje

def _enviar(mensaje: EmailMessage) -> None:
    if not os.getenv('SMTP_USER') or not os.getenv('SMTP_PASSWORD'):
        print(f"[AVISO] Mail omitido (sin credenciales SMTP): {mensaje['Subject']} -> {mensaje['To']}")
        return

    try:
        with _conectar(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT', '587'))) as conexion:
            conexion.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD', ''))
            conexion.send_message(mensaje)
    except (smtplib.SMTPException, OSError):
        raise ApiError('No se pudo enviar el mail', 502)

def enviar_entrada(destinatario: dict, entrada: dict, png: bytes):
    mensaje = _configurar_mensaje(destinatario, f"Tu entrada #{entrada['id']} - Cine Paradiso")
    detalle = (f"Te enviamos tu entrada para la función #{entrada['id_funcion']} "
               f"({str(entrada['fecha_hora_funcion']).replace('T', ' ')}), butaca {entrada['id_butaca']}.")
    url = _url_cancelacion(entrada['id'])
    mensaje.set_content(
        f"Hola {destinatario['nombre']},\n\n"
        f"{detalle}\n"
        'Presentá el código QR adjunto en la puerta de la sala.\n\n'
        f"Si no vas a poder ir, podés cancelarla hasta 2 horas antes de la función:\n{url}\n\n"
        'Cine Paradiso'
    )
    mensaje.add_alternative(
        f"<p>Hola {html.escape(destinatario['nombre'])},</p>"
        f"<p>{html.escape(detalle)}<br>Presentá el código QR adjunto en la puerta de la sala.</p>"
        "<p>Si no vas a poder ir, podés cancelarla hasta 2 horas antes de la función:</p>"
        f"<p>{_boton(url, 'Cancelar entrada')}</p>"
        f'<p style="font-size:12px; color:#666;">Si el botón no funciona, copiá este enlace: {html.escape(url)}</p>'
        "<p>Cine Paradiso</p>",
        subtype='html'
    )
    mensaje.add_attachment(png, maintype='image', subtype='png', filename=f"entrada-{entrada['id']}.png")
    _enviar(mensaje)

def enviar_compra(destinatario: dict, factura: dict, adjuntos_qr: list) -> None:
    reserva = factura['reserva']
    lineas = [f"- Entrada #{e['id']}: función #{e['id_funcion']} "
              f"({str(e['fecha_hora_funcion']).replace('T', ' ')}), butaca {e['id_butaca']} - ${e['precio']}"
              for e in factura['entradas'] if e['estado'] != 'cancelada']
    lineas += [f"- {s['nombre']} x{s['cantidad']} - ${s['subtotal']}" for s in factura['servicios']]
    # Un enlace de cancelación por cada entrada que todavía está activa
    activas = [e for e in factura['entradas'] if e['estado'] == 'activa']
    enlaces = [f"- Entrada #{e['id']} (butaca {e['id_butaca']}): {_url_cancelacion(e['id'])}" for e in activas]
    mensaje = _configurar_mensaje(destinatario, f"Compra confirmada - Reserva #{reserva['id_reserva']} - Cine Paradiso")
    mensaje.set_content(
        f"Hola {destinatario['nombre']},\n\n"
        "Tu compra fue confirmada. Detalle de la factura:\n\n"
        + '\n'.join(lineas)
        + f"\n\nTotal: ${factura['total']}\n\n"
        "Adjuntamos los códigos QR de tus entradas. Recordá que podés cancelarlas "
        "hasta 2 horas antes de la función desde la sección 'Mis entradas'"
        + (" o con estos enlaces:\n" + '\n'.join(enlaces) if enlaces else '.')
        + '\n\nCine Paradiso'
    )
    botones = ''.join(
        f"<p>Entrada #{e['id']} (butaca {html.escape(str(e['id_butaca']))}): "
        f"{_boton(_url_cancelacion(e['id']), 'Cancelar entrada #' + str(e['id']))}</p>"
        for e in activas
    )
    mensaje.add_alternative(
        f"<p>Hola {html.escape(destinatario['nombre'])},</p>"
        "<p>Tu compra fue confirmada. Detalle de la factura:</p>"
        "<ul>" + ''.join(f"<li>{html.escape(linea[2:])}</li>" for linea in lineas) + "</ul>"
        f"<p><b>Total: ${html.escape(str(factura['total']))}</b></p>"
        "<p>Adjuntamos los códigos QR de tus entradas. Recordá que podés cancelarlas "
        "hasta 2 horas antes de la función desde la sección 'Mis entradas' o con estos botones:</p>"
        + botones
        + '<p style="font-size:12px; color:#666;">Si un botón no funciona, usá los enlaces de la versión de texto '
          'o entrá a "Mis entradas".</p>'
        "<p>Cine Paradiso</p>",
        subtype='html'
    )
    for id_entrada, png in adjuntos_qr:
        mensaje.add_attachment(png, maintype='image', subtype='png', filename=f"entrada-{id_entrada}.png")
    _enviar(mensaje)

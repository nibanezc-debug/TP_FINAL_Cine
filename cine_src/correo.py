import os
import smtplib
from email.message import EmailMessage
from errors import ApiError

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
    try:
        with _conectar(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT', '587'))) as conexion:
            if os.getenv('SMTP_USER'):
                conexion.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD', ''))
            conexion.send_message(mensaje)
    except (smtplib.SMTPException, OSError):
        raise ApiError('No se pudo enviar el mail', 502)

def enviar_entrada(destinatario: dict, entrada: dict, png: bytes):
    mensaje = _configurar_mensaje(destinatario, f"Tu entrada #{entrada['id']} - Cine Paradiso")
    mensaje.set_content(
        f"Hola {destinatario['nombre']},\n\n"
        f"Te enviamos tu entrada para la función #{entrada['id_funcion']} "
        f"({str(entrada['fecha_hora_funcion']).replace('T', ' ')}), butaca {entrada['id_butaca']}.\n"
        'Presentá el código QR adjunto en la puerta de la sala.\n\nCine Paradiso'
    )
    mensaje.add_attachment(png, maintype='image', subtype='png', filename=f"entrada-{entrada['id']}.png")
    _enviar(mensaje)

def enviar_compra(destinatario: dict, factura: dict, adjuntos_qr: list) -> None:
    reserva = factura['reserva']
    lineas = [f"- Entrada #{e['id']}: función #{e['id_funcion']} "
              f"({str(e['fecha_hora_funcion']).replace('T', ' ')}), butaca {e['id_butaca']} - ${e['precio']}"
              for e in factura['entradas'] if e['estado'] != 'cancelada']
    lineas += [f"- {s['nombre']} x{s['cantidad']} - ${s['subtotal']}" for s in factura['servicios']]
    mensaje = _configurar_mensaje(destinatario, f"Compra confirmada - Reserva #{reserva['id_reserva']} - Cine Paradiso")
    mensaje.set_content(
        f"Hola {destinatario['nombre']},\n\n"
        "Tu compra fue confirmada. Detalle de la factura:\n\n"
        + '\n'.join(lineas)
        + f"\n\nTotal: ${factura['total']}\n\n"
        "Adjuntamos los códigos QR de tus entradas. Recordá que podés cancelarlas "
        "hasta 2 horas antes de la función desde la sección 'Mis entradas'.\n\n"
        'Cine Paradiso'
    )
    for id_entrada, png in adjuntos_qr:
        mensaje.add_attachment(png, maintype='image', subtype='png', filename=f"entrada-{id_entrada}.png")
    _enviar(mensaje)

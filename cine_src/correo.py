import os
import smtplib
from email.message import EmailMessage
from cine_src.errors import ApiError

def _conectar(servidor: str, puerto: int):
    if puerto == 465:
        return smtplib.SMTP_SSL(servidor, puerto, timeout=10)
    conexion = smtplib.SMTP(servidor, puerto, timeout=10)
    conexion.starttls()
    return conexion

def enviar_entrada(destinatario: dict, entrada: dict, png: bytes):
    servidor = os.getenv('SMTP_HOST')
    remitente = os.getenv('SMTP_FROM') or os.getenv('SMTP_USER')
    if not servidor or not remitente:
        raise ApiError('El envío de mails no está configurado', 503)
    mensaje = EmailMessage()
    mensaje['Subject'] = f"Tu entrada #{entrada['id']} - Cine Paradiso"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario['email']
    mensaje.set_content(
        f"Hola {destinatario['nombre']},\n\n"
        f"Te enviamos tu entrada para la función #{entrada['id_funcion']} "
        f"({str(entrada['fecha_hora_funcion']).replace('T', ' ')}), butaca {entrada['id_butaca']}.\n"
        'Presentá el código QR adjunto en la puerta de la sala.\n\nCine Paradiso'
    )
    mensaje.add_attachment(png, maintype='image', subtype='png', filename=f"entrada-{entrada['id']}.png")
    try:
        with _conectar(servidor, int(os.getenv('SMTP_PORT', '587'))) as conexion:
            if os.getenv('SMTP_USER'):
                conexion.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD', ''))
            conexion.send_message(mensaje)
    except (smtplib.SMTPException, OSError):
        raise ApiError('No se pudo enviar el mail', 502)

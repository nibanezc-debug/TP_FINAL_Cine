import requests
from flask import abort, current_app, session

CODIGOS_ERROR = (400, 401, 403, 404, 405, 409, 422, 500, 502, 503)


def llamar_api(metodo, ruta, con_sesion=True, **kwargs):
    url = f"{current_app.config['API_URL']}{ruta}"
    cookies = (session.get("api_cookies") or {}) if con_sesion else {}
    try:
        resp = requests.request(metodo, url, cookies=cookies, timeout=5, **kwargs)
    except requests.exceptions.RequestException:
        abort(503, description="No se pudo conectar con el backend")

    try:
        datos = resp.json()
    except ValueError:
        datos = None

    if not resp.ok:
        mensaje = datos.get("error") if isinstance(datos, dict) else None
        estado = resp.status_code if resp.status_code in CODIGOS_ERROR else 502
        abort(estado, description=mensaje or "Error en el backend")
    return datos, resp
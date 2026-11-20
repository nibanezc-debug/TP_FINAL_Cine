"""Pruebas de la confirmación de cancelación y del regreso después del login.

Se corren desde API_FRONTEND:  python -m unittest discover -s tests
El backend se simula reemplazando requests.request, así que no se toca la base.
"""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("FLASK_SECRET_KEY", "clave-para-pruebas")

from app import crear_app  # noqa: E402
from web.routes.site.auth import destino_seguro  # noqa: E402

ENTRADA = {"id": 7, "id_funcion": 1, "id_butaca": 11, "precio": 6900, "estado": "activa",
           "codigo_qr": "abc", "fecha_hora_funcion": "2026-11-25T20:00:00"}
FUNCION = {"id": 1, "titulo": "The Matrix", "local": "Alto Palermo", "sala": "Sala 1"}
BUTACAS = [{"id": 11, "fila": "A", "columna": 11}]


class Respuesta:
    def __init__(self, estado, datos):
        self.status_code, self._datos, self.ok = estado, datos, estado < 400
        self.cookies = type("Cookies", (), {"get_dict": lambda self: {"session": "x"}})()

    def json(self):
        return self._datos


def backend(estado_entrada="activa", detalle=None):
    llamadas = []

    def falso(metodo, url, **kwargs):
        ruta = url.split("/api", 1)[1]
        llamadas.append((metodo, ruta))
        if ruta == "/auth/login":
            return Respuesta(200, {"id_usuario": 2, "email": "c@x", "rol": "cliente"})
        if ruta == "/usuarios/login":
            return Respuesta(404, {"error": "no existe"})
        if ruta == "/entradas/7" and metodo == "GET":
            return detalle or Respuesta(200, {**ENTRADA, "estado": estado_entrada})
        if ruta == "/funciones/1":
            return Respuesta(200, FUNCION)
        if ruta == "/funciones/1/butacas":
            return Respuesta(200, BUTACAS)
        if ruta == "/entradas/7/cancelar" and metodo == "PATCH":
            return Respuesta(200, {**ENTRADA, "estado": "cancelada"})
        if ruta == "/entradas/mias":
            return Respuesta(200, [])
        return Respuesta(404, {"error": "no simulado"})
    return falso, llamadas


class PruebasConfirmacionCancelacion(unittest.TestCase):
    def setUp(self):
        app = crear_app()
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def iniciar_sesion(self):
        with self.cliente.session_transaction() as s:
            s.update(usuario_id=2, rol="cliente", email="c@x", api_cookies={"session": "x"})

    def test_sin_sesion_manda_al_login_con_destino(self):
        respuesta = self.cliente.get("/entradas/7/cancelar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.location.endswith("/login?next=/entradas/7/cancelar"))

    def test_get_muestra_la_entrada_y_no_cancela(self):
        self.iniciar_sesion()
        falso, llamadas = backend()
        with patch("api_client.requests.request", side_effect=falso):
            respuesta = self.cliente.get("/entradas/7/cancelar")
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("The Matrix", html)
        self.assertIn("<b>A11</b>", html)
        self.assertIn('action="/entradas/7/cancelar" method="post"', html)
        self.assertNotIn("PATCH", [metodo for metodo, _ in llamadas])

    def test_entrada_usada_no_ofrece_cancelar(self):
        self.iniciar_sesion()
        falso, _ = backend("usada")
        with patch("api_client.requests.request", side_effect=falso):
            html = self.cliente.get("/entradas/7/cancelar").get_data(as_text=True)
        self.assertNotIn("Sí, cancelar entrada", html)
        self.assertIn("ya no se puede cancelar", html)

    def test_entrada_ajena_o_inexistente_muestra_error(self):
        self.iniciar_sesion()
        for estado, mensaje in ((403, "No podés acceder a esta entrada"), (404, "La entrada no existe")):
            falso, _ = backend(detalle=Respuesta(estado, {"error": mensaje}))
            with patch("api_client.requests.request", side_effect=falso):
                respuesta = self.cliente.get("/entradas/7/cancelar")
            self.assertEqual(respuesta.status_code, estado)
            self.assertIn(mensaje, respuesta.get_data(as_text=True))

    def test_post_cancela_con_el_llamado_existente(self):
        self.iniciar_sesion()
        falso, llamadas = backend()
        with patch("api_client.requests.request", side_effect=falso):
            respuesta = self.cliente.post("/entradas/7/cancelar")
        self.assertTrue(respuesta.location.endswith("/entradas"))
        self.assertIn(("PATCH", "/entradas/7/cancelar"), llamadas)


class PruebasRegresoLogin(unittest.TestCase):
    def setUp(self):
        app = crear_app()
        app.config["TESTING"] = True
        self.cliente = app.test_client()

    def login(self, destino):
        falso, _ = backend()
        with patch("api_client.requests.request", side_effect=falso):
            return self.cliente.post("/login", data={"email": "c@x", "password": "x", "next": destino})

    def test_vuelve_al_destino_interno(self):
        respuesta = self.login("/entradas/7/cancelar")
        self.assertTrue(respuesta.location.endswith("/entradas/7/cancelar"))

    def test_rechaza_destinos_externos(self):
        for destino in ("https://otro.com", "//otro.com", "/\\otro.com", "/\t/otro.com", "javascript:alert(1)", "otro.com"):
            with self.subTest(destino=destino):
                self.assertIsNone(destino_seguro(destino))
                respuesta = self.login(destino)
                self.assertTrue(respuesta.location.endswith("/cartelera"), respuesta.location)

    def test_formulario_conserva_el_destino(self):
        html = self.cliente.get("/login?next=/entradas/7/cancelar").get_data(as_text=True)
        self.assertIn('name="next" value="/entradas/7/cancelar"', html)
        html = self.cliente.get("/login?next=https://otro.com").get_data(as_text=True)
        self.assertNotIn('name="next"', html)


if __name__ == "__main__":
    unittest.main()

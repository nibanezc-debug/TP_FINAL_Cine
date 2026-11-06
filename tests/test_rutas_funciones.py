import os
import unittest
from unittest.mock import patch

os.environ.setdefault("FLASK_SECRET_KEY", "clave-local-para-pruebas-unitarias")

from app import crear_app


class PruebasHttpFunciones(unittest.TestCase):
    def setUp(self):
        self.cliente = crear_app().test_client()

    def test_post_requiere_login(self):
        respuesta = self.cliente.post("/api/funciones", json={"precio": 5000})
        self.assertEqual(respuesta.status_code, 401)

    @patch("security.usuario_actual", return_value={"id": 1, "rol": "cliente"})
    def test_cliente_no_puede_crear(self, _):
        respuesta = self.cliente.post("/api/funciones", json={"precio": 5000})
        self.assertEqual(respuesta.status_code, 403)

    @patch("security.usuario_actual", return_value={"id": 1, "rol": "administrador"})
    def test_admin_sin_json_recibe_400(self, _):
        respuesta = self.cliente.post("/api/funciones", data="no json", content_type="text/plain")
        self.assertEqual(respuesta.status_code, 400)

    @patch("security.usuario_actual", return_value={"id": 1, "rol": "administrador"})
    @patch("routes.funciones.servicio.crear_funcion", return_value={"id": 8})
    def test_post_devuelve_201(self, crear, _):
        respuesta = self.cliente.post("/api/funciones", json={"id_sala": 2})
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.get_json(), {"id": 8})
        crear.assert_called_once_with({"id_sala": 2})

    @patch("security.usuario_actual", return_value={"id": 1, "rol": "administrador"})
    @patch("routes.funciones.servicio.modificar_funcion")
    def test_patch_devuelve_204(self, modificar, _):
        respuesta = self.cliente.patch("/api/funciones/8", json={"precio": 7000})
        self.assertEqual(respuesta.status_code, 204)
        modificar.assert_called_once_with(8, {"precio": 7000})

    @patch("security.usuario_actual", return_value={"id": 1, "rol": "administrador"})
    @patch("routes.funciones.servicio.eliminar_funcion")
    def test_delete_devuelve_204(self, eliminar, _):
        respuesta = self.cliente.delete("/api/funciones/8")
        self.assertEqual(respuesta.status_code, 204)
        eliminar.assert_called_once_with(8)


if __name__ == "__main__":
    unittest.main()

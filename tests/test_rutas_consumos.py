import os
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_SECRET_KEY', 'clave-local-para-pruebas-unitarias')

from cine_src.app import crear_app


class PruebasHttpConsumos(unittest.TestCase):
    def setUp(self):
        self.cliente = crear_app().test_client()

    def test_sin_autenticacion_devuelve_401(self):
        respuesta = self.cliente.get('/api/reservas/1/consumos')
        self.assertEqual(respuesta.status_code, 401)

    @patch('cine_src.routes.consumos.usuario_actual', return_value={'id': 8, 'rol': 'cliente'})
    def test_cantidad_incorrecta(self, actual):
        respuesta = self.cliente.post('/api/reservas/1/consumos', json={'id_servicio': 2, 'cantidad': 0})
        self.assertEqual(respuesta.status_code, 400)

    @patch('cine_src.routes.consumos.usuario_actual', return_value={'id': 8, 'rol': 'cliente'})
    def test_json_invalido(self, actual):
        respuesta = self.cliente.post('/api/reservas/1/consumos', data='texto', content_type='text/plain')
        self.assertEqual(respuesta.status_code, 400)


if __name__ == '__main__':
    unittest.main()

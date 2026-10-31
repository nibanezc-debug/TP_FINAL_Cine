import os
import unittest
from unittest.mock import patch

os.environ.setdefault('FLASK_SECRET_KEY', 'clave-local-para-pruebas-unitarias')

from cine_src.app import crear_app


class PruebasHttpServicios(unittest.TestCase):
    def setUp(self):
        self.cliente = crear_app().test_client()

    def test_sin_autenticacion_devuelve_401(self):
        respuesta = self.cliente.get('/api/servicios')
        self.assertEqual(respuesta.status_code, 401)

    @patch('cine_src.security.usuario_actual', return_value={'id': 1, 'rol': 'cliente'})
    @patch('cine_src.services.servicios.repositorio.listar', return_value=[])
    def test_listar_vacio(self, listar, actual):
        respuesta = self.cliente.get('/api/servicios')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json(), [])

    @patch('cine_src.security.usuario_actual', return_value={'id': 1, 'rol': 'cliente'})
    def test_cliente_no_puede_crear(self, actual):
        respuesta = self.cliente.post('/api/servicios', json={'nombre': 'Combo', 'precio': 5000})
        self.assertEqual(respuesta.status_code, 403)

    @patch('cine_src.security.usuario_actual', return_value={'id': 1, 'rol': 'administrador'})
    def test_creacion_sin_body(self, actual):
        respuesta = self.cliente.post('/api/servicios', data='sin-json', content_type='text/plain')
        self.assertEqual(respuesta.status_code, 400)


if __name__ == '__main__':
    unittest.main()

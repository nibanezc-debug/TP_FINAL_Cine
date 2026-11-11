import unittest
from unittest.mock import patch

from cine_src.errors import ApiError
from cine_src.services import usuarios as servicio
from cine_src.validators.usuarios import (
    validar_id,
    validar_registro,
    validar_login,
    validar_actualizacion
)


class PruebasUsuarios(unittest.TestCase):

    def setUp(self):
        self.cliente = {'id': 1, 'rol': 'cliente'}
        self.otro_cliente = {'id': 2, 'rol': 'cliente'}
        self.admin = {'id': 99, 'rol': 'administrador'}

    def test_validar_registro_correcto(self):
        datos = {'nombre': '  Thiago  ', 'email': 'THIAGO@CINE.COM', 'password': '123'}
        resultado = validar_registro(datos)
        self.assertEqual(resultado['nombre'], 'Thiago')
        self.assertEqual(resultado['email'], 'thiago@cine.com')

    def test_validar_registro_email_invalido(self):
        with self.assertRaises(ApiError) as error:
            validar_registro({'nombre': 'Thiago', 'email': 'email_sin_arroba', 'password': '123'})
        self.assertEqual(error.exception.estado, 400)

    def test_validar_id_invalido(self):
        with self.assertRaises(ApiError) as error:
            validar_id(-5)
        self.assertEqual(error.exception.estado, 400)
        
    @patch.object(servicio.repositorio, 'buscar_por_email', return_value=None)
    def test_login_usuario_inexistente_es_401(self, _):
        with self.assertRaises(ApiError) as error:
            servicio.login({'email': 'noexiste@cine.com', 'password': '123'})
        self.assertEqual(error.exception.estado, 401)

    @patch.object(servicio.repositorio, 'buscar_por_id', return_value={'id': 1, 'nombre': 'Thiago', 'email': 't@cine.com', 'password': 'secret_pass', 'rol': 'cliente'})
    def test_obtener_perfil_propio(self, _):
        perfil = servicio.obtener_por_id(1, self.cliente)
        self.assertEqual(perfil['id'], 1)
        self.assertNotIn('password', perfil)  # Verifica que se remueva la clave

    def test_obtener_perfil_ajeno_rechaza_cliente(self):
        with self.assertRaises(ApiError) as error:
            servicio.obtener_por_id(2, self.cliente)
        self.assertEqual(error.exception.estado, 403)

    @patch.object(servicio.repositorio, 'buscar_por_id', return_value={'id': 2, 'nombre': 'Pedro', 'email': 'p@cine.com', 'password': '123', 'rol': 'cliente'})
    def test_obtener_perfil_ajeno_permite_admin(self, _):
        perfil = servicio.obtener_por_id(2, self.admin)
        self.assertEqual(perfil['id'], 2)


if __name__ == '__main__':
    unittest.main()
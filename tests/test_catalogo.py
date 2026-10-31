import unittest
from unittest.mock import patch
from cine_src.errors import ApiError
from cine_src.validators.servicios import validar_servicio
from cine_src.services import servicios

class PruebasCatalogo(unittest.TestCase):

    def test_valida_servicio(self):
        self.assertEqual(validar_servicio({'nombre': ' Pochoclos ', 'precio': 2000}), {'nombre': 'Pochoclos', 'precio': 2000})

    def test_rechaza_booleano_como_precio(self):
        with self.assertRaises(ApiError):
            validar_servicio({'nombre': 'Combo', 'precio': True})

    def test_rechaza_precio_negativo(self):
        with self.assertRaises(ApiError):
            validar_servicio({'nombre': 'Combo', 'precio': -4})

    @patch.object(servicios.repositorio, 'buscar', return_value=None)
    def test_servicio_inexistente_es_404(self, _):
        with self.assertRaises(ApiError) as error:
            servicios.buscar(33)
        self.assertEqual(error.exception.estado, 404)

    @patch.object(servicios.repositorio, 'insertar', return_value=7)
    @patch.object(servicios.repositorio, 'buscar', return_value={'id': 7, 'nombre': 'Combo', 'precio': 1250})
    def test_creacion_utiliza_repositorio(self, buscar, insertar):
        resultado = servicios.crear({'nombre': 'Combo', 'precio': 1250})
        self.assertEqual(resultado['id'], 7)
        insertar.assert_called_once_with('Combo', 1250)
if __name__ == '__main__':
    unittest.main()

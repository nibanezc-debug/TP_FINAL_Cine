import unittest
from unittest.mock import patch
from cine_src.errors import ApiError
from cine_src.services import consumos

class PruebasConsumos(unittest.TestCase):

    def setUp(self):
        self.cliente = {'id': 8, 'rol': 'cliente'}

    @patch.object(consumos.repositorio, 'obtener_reserva', return_value={'id': 1, 'id_usuario': 8, 'estado': 'pendiente'})
    @patch.object(consumos.repositorio, 'listar', return_value=[])
    def test_listar_reserva_propia(self, listar, _):
        self.assertEqual(consumos.listar(1, self.cliente), [])
        listar.assert_called_once_with(1)

    @patch.object(consumos.repositorio, 'obtener_reserva', return_value={'id': 1, 'id_usuario': 15, 'estado': 'pendiente'})
    def test_no_lista_reserva_ajena(self, _):
        with self.assertRaises(ApiError) as error:
            consumos.listar(1, self.cliente)
        self.assertEqual(error.exception.estado, 403)

    def test_rechaza_cantidad_cero(self):
        with self.assertRaises(ApiError) as error:
            consumos.agregar(1, self.cliente, {'id_servicio': 2, 'cantidad': 0})
        self.assertEqual(error.exception.estado, 400)

    def test_no_acepta_cantidad_booleana(self):
        with self.assertRaises(ApiError):
            consumos.agregar(1, self.cliente, {'id_servicio': 2, 'cantidad': True})

    @patch.object(consumos.repositorio, 'agregar', return_value={'id': 3, 'id_reserva': 1, 'id_servicio': 2, 'cantidad': 1, 'precio_unitario': 5000, 'subtotal': 5000})
    def test_agregar_llama_repositorio(self, agregar):
        dato = consumos.agregar(1, self.cliente, {'id_servicio': 2, 'cantidad': 1})
        self.assertEqual(dato['subtotal'], 5000)
        agregar.assert_called_once_with(1, 8, 2, 1)
if __name__ == '__main__':
    unittest.main()

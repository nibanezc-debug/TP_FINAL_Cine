import unittest
from datetime import datetime
from unittest.mock import patch

from errors import ApiError
from services import funciones as servicio
from validators.funciones import validar_datos_funcion


DATOS = {
    "id_pelicula": 1,
    "id_sala": 2,
    "fecha_hora": "2035-11-10 20:00:00",
    "precio": 5000,
}
PELICULA = {
    "activa": True,
    "duracion_minutos": 120,
    "disponible_desde": None,
    "disponible_hasta": None,
}
ACTUAL = {
    **DATOS,
    "id": 7,
    "fecha_hora": datetime(2035, 11, 10, 20, 0, 0),
}


class PruebasFunciones(unittest.TestCase):
    def test_post_requiere_todos_los_campos(self):
        with self.assertRaises(ApiError) as error:
            validar_datos_funcion({"precio": 5000})
        self.assertEqual(error.exception.estado, 400)

    def test_patch_acepta_datos_parciales(self):
        self.assertEqual(validar_datos_funcion({"precio": 6000}, es_patch=True), {"precio": 6000})

    def test_rechaza_precio_booleano(self):
        with self.assertRaises(ApiError):
            validar_datos_funcion({**DATOS, "precio": True})

    def test_rechaza_fecha_invalida(self):
        with self.assertRaises(ApiError):
            validar_datos_funcion({**DATOS, "fecha_hora": "2035-15-99"})

    def test_rechaza_campos_desconocidos(self):
        with self.assertRaises(ApiError):
            validar_datos_funcion({**DATOS, "descuento": 20})

    def test_crear_funcion_devuelve_id(self):
        with patch.object(servicio.repositorio, "buscar_pelicula", return_value=PELICULA), \
             patch.object(servicio.repositorio, "buscar_sala", return_value={"id": 2}), \
             patch.object(servicio.repositorio, "hay_superposicion", return_value=False), \
             patch.object(servicio.repositorio, "crear_funcion", return_value=9) as crear:
            self.assertEqual(servicio.crear_funcion(DATOS), {"id": 9})
            crear.assert_called_once_with(DATOS)

    def test_no_permite_superposicion(self):
        with patch.object(servicio.repositorio, "buscar_pelicula", return_value=PELICULA), \
             patch.object(servicio.repositorio, "buscar_sala", return_value={"id": 2}), \
             patch.object(servicio.repositorio, "hay_superposicion", return_value=True):
            with self.assertRaises(ApiError) as error:
                servicio.crear_funcion(DATOS)
            self.assertEqual(error.exception.estado, 409)

    def test_patch_conserva_datos_no_enviados(self):
        with patch.object(servicio.repositorio, "buscar_funcion_por_id", return_value=ACTUAL), \
             patch.object(servicio.repositorio, "tiene_entradas", return_value=False), \
             patch.object(servicio.repositorio, "buscar_pelicula", return_value=PELICULA), \
             patch.object(servicio.repositorio, "buscar_sala", return_value={"id": 2}), \
             patch.object(servicio.repositorio, "hay_superposicion", return_value=False), \
             patch.object(servicio.repositorio, "modificar_funcion") as modificar:
            servicio.modificar_funcion(7, {"precio": 6000})
            modificar.assert_called_once_with(7, {"precio": 6000})

    def test_no_modifica_si_tiene_entradas(self):
        with patch.object(servicio.repositorio, "buscar_funcion_por_id", return_value=ACTUAL), \
             patch.object(servicio.repositorio, "tiene_entradas", return_value=True):
            with self.assertRaises(ApiError) as error:
                servicio.modificar_funcion(7, {"precio": 6000})
            self.assertEqual(error.exception.estado, 409)

    def test_no_elimina_si_tiene_entradas(self):
        with patch.object(servicio.repositorio, "buscar_funcion_por_id", return_value=ACTUAL), \
             patch.object(servicio.repositorio, "tiene_entradas", return_value=True):
            with self.assertRaises(ApiError) as error:
                servicio.eliminar_funcion(7)
            self.assertEqual(error.exception.estado, 409)

    def test_eliminar_funcion_libre(self):
        with patch.object(servicio.repositorio, "buscar_funcion_por_id", return_value=ACTUAL), \
             patch.object(servicio.repositorio, "tiene_entradas", return_value=False), \
             patch.object(servicio.repositorio, "eliminar_funcion") as eliminar:
            servicio.eliminar_funcion(7)
            eliminar.assert_called_once_with(7)

    def test_funcion_inexistente_es_404(self):
        with patch.object(servicio.repositorio, "buscar_funcion_por_id", return_value=None):
            with self.assertRaises(ApiError) as error:
                servicio.eliminar_funcion(999)
            self.assertEqual(error.exception.estado, 404)


if __name__ == "__main__":
    unittest.main()

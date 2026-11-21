"""Pruebas de los enlaces de cancelación en los correos.

Se corren con cine_src en el path (igual que test_funciones):
    PYTHONPATH=cine_src python -m unittest tests.test_correo
_enviar se reemplaza, así que no se manda ningún correo.
"""
import os
import unittest
from unittest.mock import patch

import correo

ENTORNO = {'SMTP_HOST': 'smtp.prueba', 'SMTP_FROM': 'cine@prueba', 'FRONTEND_URL': 'https://cine.ejemplo.com/'}
USUARIO = {'nombre': 'Ana <b>&</b>', 'email': 'ana@prueba'}


def partes(mensaje):
    texto = mensaje.get_body(preferencelist=('plain',)).get_content()
    html = mensaje.get_body(preferencelist=('html',)).get_content()
    adjuntos = [a.get_filename() for a in mensaje.iter_attachments()]
    return texto, html, adjuntos


class PruebasCorreo(unittest.TestCase):
    @patch.dict(os.environ, ENTORNO)
    @patch('correo._enviar')
    def test_entrada_tiene_boton_y_enlace(self, enviar):
        entrada = {'id': 7, 'id_funcion': 1, 'fecha_hora_funcion': '2026-11-25T20:00:00', 'id_butaca': 11}
        correo.enviar_entrada(USUARIO, entrada, b'png')
        texto, html, adjuntos = partes(enviar.call_args[0][0])
        url = 'https://cine.ejemplo.com/entradas/7/cancelar'
        self.assertIn(url, texto)
        self.assertIn(f'href="{url}"', html)
        self.assertIn('Cancelar entrada', html)
        self.assertIn('Ana &lt;b&gt;&amp;&lt;/b&gt;', html)
        self.assertNotIn('<b>&</b>', html)
        self.assertEqual(adjuntos, ['entrada-7.png'])

    @patch.dict(os.environ, ENTORNO)
    @patch('correo._enviar')
    def test_compra_tiene_un_enlace_por_entrada_activa(self, enviar):
        factura = {
            'reserva': {'id_reserva': 3},
            'entradas': [
                {'id': 7, 'id_funcion': 1, 'fecha_hora_funcion': '2026-11-25T20:00:00', 'id_butaca': 11, 'precio': 6900, 'estado': 'activa'},
                {'id': 8, 'id_funcion': 1, 'fecha_hora_funcion': '2026-11-25T20:00:00', 'id_butaca': 12, 'precio': 6900, 'estado': 'activa'},
                {'id': 9, 'id_funcion': 1, 'fecha_hora_funcion': '2026-11-25T20:00:00', 'id_butaca': 13, 'precio': 6900, 'estado': 'cancelada'},
            ],
            'servicios': [{'nombre': 'Combo <Pop>', 'cantidad': 1, 'subtotal': 12900}],
            'total': 26700,
        }
        correo.enviar_compra(USUARIO, factura, [(7, b'png'), (8, b'png')])
        texto, html, adjuntos = partes(enviar.call_args[0][0])
        for id_entrada in (7, 8):
            url = f'https://cine.ejemplo.com/entradas/{id_entrada}/cancelar'
            self.assertIn(f'Entrada #{id_entrada}', texto)
            self.assertIn(url, texto)
            self.assertIn(f'href="{url}"', html)
            self.assertIn(f'Cancelar entrada #{id_entrada}', html)
        self.assertNotIn('/entradas/9/cancelar', texto + html)
        self.assertIn('Total: $26700', texto)
        self.assertIn('Combo &lt;Pop&gt;', html)
        self.assertEqual(adjuntos, ['entrada-7.png', 'entrada-8.png'])

    @patch.dict(os.environ, {'SMTP_HOST': 'smtp.prueba', 'SMTP_FROM': 'cine@prueba'})
    @patch('correo._enviar')
    def test_sin_frontend_url_usa_localhost(self, enviar):
        os.environ.pop('FRONTEND_URL', None)
        entrada = {'id': 5, 'id_funcion': 1, 'fecha_hora_funcion': '2026-11-25T20:00:00', 'id_butaca': 11}
        correo.enviar_entrada(USUARIO, entrada, b'png')
        texto, _, _ = partes(enviar.call_args[0][0])
        self.assertIn('http://127.0.0.1:5001/entradas/5/cancelar', texto)


if __name__ == '__main__':
    unittest.main()

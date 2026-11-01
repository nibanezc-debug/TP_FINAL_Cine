
from cine_src.repositories import locales as repositories

REQUERIDOS_LOCAL = ['nombre', 'direccion']
TIPOS_LOCAL = {
    'nombre': str,
    'direccion': str
}

def validar_data_locales(data, es_patch=False):
    if not isinstance(data, dict) or not data:
        return False, {'error': 'Debe enviar un objeto JSON válido con datos'}, 400

    if not es_patch:
        for campo in REQUERIDOS_LOCAL:
            if campo not in data or data[campo] is None or data[campo] == '':
                return False, {'error': f'El campo "{campo}" es obligatorio'}, 400

    for campo, valor in data.items():
        if campo in TIPOS_LOCAL:
            tipo_esperado = TIPOS_LOCAL[campo]
            if not isinstance(valor, tipo_esperado):
                return False, {'error': f'El campo "{campo}" debe ser de tipo {tipo_esperado.__name__}'}, 400
            if es_patch and valor == '':
                return False, {'error': f'El campo "{campo}" no puede estar vacío'}, 400

    return True, None, 200


def local_tiene_salas(id_local):
    return repositories.contar_salas_de_local(id_local) > 0
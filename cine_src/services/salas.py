from cine_src.repositories import salas as repositories

REQUERIDOS_SALA = ['nombre', 'capacidad', 'formato']
TIPOS_SALA = {
    'nombre': str,
    'capacidad': int,
    'formato': str
}

def validar_data_salas(data, es_patch=False):
    if not isinstance(data, dict) or not data:
        return False, {'error': 'Debe enviar un objeto JSON válido con datos'}, 400

    if not es_patch:
        for campo in REQUERIDOS_SALA:
            if campo not in data or data[campo] is None or data[campo] == '':
                return False, {'error': f'El campo "{campo}" es obligatorio'}, 400

    for campo, valor in data.items():
        if campo in TIPOS_SALA:
            tipo_esperado = TIPOS_SALA[campo]
            if not isinstance(valor, tipo_esperado):
                return False, {'error': f'El campo "{campo}" debe ser de tipo {tipo_esperado.__name__}'}, 400

    return True, None, 200


def sala_activa(id_sala):
    return repositories.buscar_sala_en_funciones(id_sala) is not None


def listar_salas_por_local(id_local, formato=None, capacidad=None, limit=10, offset=0):
    salas = repositories.listar_salas_por_local(id_local, formato, capacidad, limit, offset)
    total = repositories.contar_total_salas(id_local, formato, capacidad)
    return salas, total
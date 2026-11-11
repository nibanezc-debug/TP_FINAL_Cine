from repositories import salas as repositories

CAPACIDADES_PERMITIDAS = {120, 250, 450}

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

            if isinstance(valor, str) and not valor.strip():
                return False, {'error': f'El campo "{campo}" no puede estar vacío'}, 400

    if 'capacidad' in data and data['capacidad'] is not None:
        if data['capacidad'] not in CAPACIDADES_PERMITIDAS:
            return False, {
                'error': f"La capacidad '{data['capacidad']}' no es válida. Las opciones permitidas son: 120, 250 o 450."
            }, 400

    return True, None, 200


def sala_activa(id_sala):
    return repositories.buscar_sala_en_funciones(id_sala) is not None


def calcular_paginacion(args):
    try:
        page = max(1, int(args.get('page', 1)))
    except (ValueError, TypeError):
        page = 1

    try:
        limit = max(1, min(100, int(args.get('limit', 10)))) 
    except (ValueError, TypeError):
        limit = 10

    offset = (page - 1) * limit
    return page, limit, offset


def obtener_salas_por_local_paginado(id_local, params_url):
    page, limit, offset = calcular_paginacion(params_url)

    formato = params_url.get('formato')
    capacidad_raw = params_url.get('capacidad')

    capacidad = None
    if capacidad_raw is not None and capacidad_raw != '':
        try:
            capacidad = int(capacidad_raw)
        except (ValueError, TypeError):
            capacidad = None

    salas = repositories.listar_salas_por_local(
        id_local=id_local,
        formato=formato,
        capacidad=capacidad,
        limit=limit,
        offset=offset
    )

    total_registros = repositories.contar_total_salas(
        id_local=id_local,
        formato=formato,
        capacidad=capacidad
    )

    total_paginas = (total_registros + limit - 1) // limit if total_registros > 0 else 1

    return {
        'items': salas,
        'paginacion': {
            'total_registros': total_registros,
            'total_paginas': total_paginas,
            'pagina_actual': page,
            'limite_por_pagina': limit,
            'tiene_siguiente': page < total_paginas,
            'tiene_anterior': page > 1
        }
    }
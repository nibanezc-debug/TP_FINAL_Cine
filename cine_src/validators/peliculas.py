from datetime import datetime
from cine_src.errors import ApiError

def validar_id(valor, nombre: str = 'id') -> int:
    if type(valor) is not int or valor <= 0:
        raise ApiError(f'El {nombre} debe ser un entero positivo', 400)
    return valor

def validar_get_externas(parametros_url: dict) -> str:
    titulo = parametros_url.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        raise ApiError('Debe enviar el parámetro ?titulo para buscar', 400)
    return titulo.strip()

def validar_filtros_peliculas(argumentos: dict) -> dict:
    filtros = {}
    
    titulo = argumentos.get("titulo")
    if titulo is not None:
        if not isinstance(titulo, str) or not titulo.strip():
            raise ApiError('El filtro titulo no puede estar vacío', 400)
        filtros["titulo"] = titulo.strip()

    genero = argumentos.get("genero")
    if genero is not None:
        if not isinstance(genero, str) or not genero.strip():
            raise ApiError('El filtro genero no puede estar vacío', 400)
        filtros["genero"] = genero.strip()

    activa = argumentos.get("activa")
    if activa is not None:
        if activa.lower() not in ("true", "false", "1", "0"):
            raise ApiError('El filtro activa debe ser true o false', 400)
        filtros["activa"] = activa.lower() in ("true", "1")

    return filtros

def _validar_fecha_hora(valor: str, nombre: str) -> str:
    if not isinstance(valor, str):
        raise ApiError(f'El campo {nombre} debe ser texto', 400)
    valor = valor.strip()
    formatos = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d')
    for fmt in formatos:
        try:
            dt = datetime.strptime(valor, fmt)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
    raise ApiError(f'El campo {nombre} debe tener formato AAAA-MM-DD o AAAA-MM-DD HH:MM:SS', 400)

def _limpiar_texto_opcional(datos: dict, campo: str, max_len: int | None = None) -> str:
    valor = datos.get(campo)
    if valor is None:
        return ""
    if not isinstance(valor, str):
        raise ApiError(f'El campo {campo} debe ser una cadena de texto', 400)
    texto = valor.strip()
    if max_len is not None and len(texto) > max_len:
        raise ApiError(f'El campo {campo} debe tener hasta {max_len} caracteres', 400)
    return texto

def validar_pelicula(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
        
    titulo = datos.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip() or len(titulo.strip()) > 150:
        raise ApiError('El título es obligatorio y debe tener hasta 150 caracteres', 400)
        
    duracion = datos.get("duracion_minutos", 0)
    if type(duracion) is not int or duracion < 0 or duracion > 1000:
        raise ApiError('La duración en minutos debe ser un entero positivo válido', 400)

    desde = datos.get("disponible_desde")
    hasta = datos.get("disponible_hasta")
    if desde is not None:
        desde = _validar_fecha_hora(desde, "disponible_desde")
    if hasta is not None:
        hasta = _validar_fecha_hora(hasta, "disponible_hasta")

    if desde and hasta and desde > hasta:
        raise ApiError('La fecha disponible_desde no puede ser posterior a disponible_hasta', 400)

    return {
        "titulo": titulo.strip(),
        "sinopsis": _limpiar_texto_opcional(datos, "sinopsis"),
        "poster_url": _limpiar_texto_opcional(datos, "poster_url", 255),
        "duracion_minutos": duracion,
        "clasificacion": _limpiar_texto_opcional(datos, "clasificacion", 10),
        "genero": _limpiar_texto_opcional(datos, "genero", 50),
        "disponible_desde": desde,
        "disponible_hasta": hasta
    }
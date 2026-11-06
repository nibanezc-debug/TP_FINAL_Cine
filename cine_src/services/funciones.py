from datetime import datetime, timedelta

from cine_src.errors import ApiError
from cine_src.repositories import funciones as repositorio
from cine_src.validators.funciones import validar_datos_funcion, validar_filtros, validar_id


def buscar_funcion_por_id(id_funcion):
    validar_id(id_funcion, "id_funcion")
    funcion = repositorio.buscar_funcion_por_id(id_funcion)

    if funcion is None:
        raise ApiError("La función solicitada no existe", 404)

    funcion["fecha_hora"] = funcion["fecha_hora"].isoformat()
    return funcion


def listar_funciones(argumentos):
    filtros = validar_filtros(argumentos)
    funciones = repositorio.listar_funciones(**filtros)

    for funcion in funciones:
        funcion["fecha_hora"] = funcion["fecha_hora"].isoformat()

    return funciones


def listar_cartelera(argumentos):
    filtros = validar_filtros(argumentos)
    funciones = repositorio.listar_cartelera(
        id_local=filtros.get("id_local"),
        fecha=filtros.get("fecha"),
    )

    peliculas = {}

    for funcion in funciones:
        id_pelicula = funcion["id_pelicula"]

        if id_pelicula not in peliculas:
            peliculas[id_pelicula] = {
                "id_pelicula": id_pelicula,
                "titulo": funcion["titulo"],
                "sinopsis": funcion["sinopsis"],
                "poster_url": funcion["poster_url"],
                "duracion_minutos": funcion["duracion_minutos"],
                "clasificacion": funcion["clasificacion"],
                "funciones": [],
            }

        peliculas[id_pelicula]["funciones"].append(
            {
                "id": funcion["id"],
                "id_sala": funcion["id_sala"],
                "sala": funcion["sala"],
                "id_local": funcion["id_local"],
                "local": funcion["local"],
                "fecha_hora": funcion["fecha_hora"].isoformat(),
                "precio": funcion["precio"],
            }
        )

    return list(peliculas.values())


def _validar_programacion(datos, id_funcion=None):
    """Comprueba fecha, película, sala y que no se pisen horarios."""
    fecha = datetime.fromisoformat(datos["fecha_hora"])
    if fecha <= datetime.now():
        raise ApiError("La función debe programarse para una fecha futura", 409)

    pelicula = repositorio.buscar_pelicula(datos["id_pelicula"])
    if pelicula is None:
        raise ApiError("La película indicada no existe", 404)
    if not pelicula["activa"]:
        raise ApiError("La película no está activa", 409)

    duracion = pelicula["duracion_minutos"]
    if type(duracion) is not int or duracion <= 0:
        raise ApiError("La película debe tener una duración positiva", 409)

    desde = pelicula["disponible_desde"]
    hasta = pelicula["disponible_hasta"]
    if (desde is not None and fecha < desde) or (hasta is not None and fecha > hasta):
        raise ApiError("La fecha está fuera del período de disponibilidad de la película", 409)

    if repositorio.buscar_sala(datos["id_sala"]) is None:
        raise ApiError("La sala indicada no existe", 404)

    fin = fecha + timedelta(minutes=duracion)
    if repositorio.hay_superposicion(datos["id_sala"], fecha, fin, id_funcion):
        raise ApiError("La sala ya tiene otra función en ese horario", 409)


def crear_funcion(datos):
    datos_limpios = validar_datos_funcion(datos)
    _validar_programacion(datos_limpios)
    id_nuevo = repositorio.crear_funcion(datos_limpios)
    return {"id": id_nuevo}


def modificar_funcion(id_funcion, datos):
    validar_id(id_funcion, "id_funcion")
    datos_limpios = validar_datos_funcion(datos, es_patch=True)
    actual = repositorio.buscar_funcion_por_id(id_funcion)
    if actual is None:
        raise ApiError("La función solicitada no existe", 404)
    if repositorio.tiene_entradas(id_funcion):
        raise ApiError("No se puede modificar una función que tiene entradas emitidas", 409)

    # PATCH: se conservan los campos que no se enviaron.
    funcion_completa = {
        "id_pelicula": actual["id_pelicula"],
        "id_sala": actual["id_sala"],
        "fecha_hora": actual["fecha_hora"].strftime("%Y-%m-%d %H:%M:%S"),
        "precio": actual["precio"],
    }
    funcion_completa.update(datos_limpios)
    _validar_programacion(funcion_completa, id_funcion)
    repositorio.modificar_funcion(id_funcion, datos_limpios)


def eliminar_funcion(id_funcion):
    validar_id(id_funcion, "id_funcion")
    actual = repositorio.buscar_funcion_por_id(id_funcion)
    if actual is None:
        raise ApiError("La función solicitada no existe", 404)
    if actual["fecha_hora"] <= datetime.now():
        raise ApiError("No se puede eliminar una función pasada o iniciada", 409)
    if repositorio.tiene_entradas(id_funcion):
        raise ApiError("No se puede eliminar una función con entradas emitidas", 409)
    repositorio.eliminar_funcion(id_funcion)

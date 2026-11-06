from errors import ApiError
from repositories import funciones as repositorio
from validators.funciones import validar_filtros, validar_id


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

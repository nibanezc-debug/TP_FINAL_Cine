import os
import requests
from errors import ApiError
from repositories import peliculas as peliculas_repo

ERRORES_SIN_RESULTADOS = ("Movie not found!", "Too many results.")

def _obtener_json_omdb(parametros: dict) -> dict:
    resultado = {}
    url = "https://www.omdbapi.com/"
    
    try:
        respuesta = requests.get(url, params=parametros, timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        if datos.get("Response") == "False":
            error_msg = datos.get("Error", "Error desconocido")
            if error_msg not in ERRORES_SIN_RESULTADOS:
                raise ApiError(f"OMDB rechazó la petición: {error_msg}", 502)
        else:
            resultado = datos
            
    except requests.RequestException:
        raise ApiError("Error de red al conectar con OMDB", 502)
    except ValueError:
        raise ApiError("Respuesta inválida de OMDB (no es JSON)", 502)
        
    return resultado

def _limpiar_dato_omdb(datos: dict, clave: str) -> str:
    resultado = ""
    valor = datos.get(clave, "")
    
    if valor != "N/A":
        resultado = valor
        
    return resultado

def _mapear_datos_omdb(datos: dict, imdb_id: str) -> dict:
    duracion_str = datos.get("Runtime", "0").split(" ")[0]
    duracion = int(duracion_str) if duracion_str.isdigit() else 0
    
    resultado = {
        "imdb_id": imdb_id,
        "titulo": datos.get("Title", "")[:150],
        "sinopsis": _limpiar_dato_omdb(datos, "Plot"),
        "poster_url": _limpiar_dato_omdb(datos, "Poster")[:255],
        "duracion_minutos": duracion,
        "clasificacion": _limpiar_dato_omdb(datos, "Rated")[:10],
        "genero": _limpiar_dato_omdb(datos, "Genre")[:50]
    }
    
    return resultado

def _obtener_detalle_externo(imdb_id: str, api_key: str) -> dict:
    detalle = {}
    parametros = {"i": imdb_id, "apikey": api_key}
    
    datos_crudos = _obtener_json_omdb(parametros)
    
    if datos_crudos.get("Response") == "True":
        detalle = _mapear_datos_omdb(datos_crudos, imdb_id)
        
    return detalle

def buscar_externas(titulo: str) -> list:
    resultado = []
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        raise ApiError("API Key de OMDB no configurada en el servidor", 500)
        
    parametros = {"s": titulo, "apikey": api_key, "type": "movie"}
    datos_internet = _obtener_json_omdb(parametros)
    
    if datos_internet.get("Response") == "True":
        peliculas = datos_internet.get("Search", [])[:5]
        
        for pelicula in peliculas:
            imdb_id = pelicula.get("imdbID")
            detalle = _obtener_detalle_externo(imdb_id, api_key)
            
            if detalle:
                resultado.append(detalle)
                
    return resultado

def _obtener_y_validar_pelicula(id_pelicula: int) -> dict:
    existe = peliculas_repo.obtener_pelicula_por_id(id_pelicula)
    if existe is None:
        raise ApiError(f"No se encontró la película con ID {id_pelicula}", 404)
    return existe

def listar_peliculas(filtros: dict, rol_usuario: str) -> list:
    if rol_usuario != "administrador":
        filtros["activa"] = True
        
    resultado = peliculas_repo.listar_peliculas(filtros)
    return resultado

def obtener_pelicula_por_id(id_pelicula: int, rol_usuario: str):
    resultado = _obtener_y_validar_pelicula(id_pelicula)
    
    if rol_usuario != "administrador" and not resultado.get("activa"):
        raise ApiError(f"No se encontró la película con ID {id_pelicula}", 404)
        
    return resultado

def crear_pelicula(datos: dict) -> dict:
    id_nuevo = peliculas_repo.crear_pelicula(datos)
    return {"id": id_nuevo}

def actualizar_pelicula(id_pelicula: int, datos: dict):
    _obtener_y_validar_pelicula(id_pelicula)
    peliculas_repo.actualizar_pelicula(id_pelicula, datos)

def eliminar_pelicula(id_pelicula: int):
    _obtener_y_validar_pelicula(id_pelicula)
    peliculas_repo.eliminar_pelicula(id_pelicula)
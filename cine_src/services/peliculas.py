import os
import requests
from cine_src.errors import ApiError
from cine_src.repositories import peliculas as peliculas_repo

def buscar_externas(titulo: str) -> list:
    api_key = os.getenv("OMDB_API_KEY", "70bcc7b2")
    url = "http://www.omdbapi.com/"
    
    try:
        respuesta = requests.get(url, params={"s": titulo, "apikey": api_key, "type": "movie"}, timeout=5)
        datos_internet = respuesta.json()
    except requests.RequestException:
        raise ApiError("Error al conectar con la API externa de películas", 502)
    
    resultado = []
    if datos_internet.get("Response") == "True":
        for item in datos_internet.get("Search", [])[:5]:
            imdb_id = item.get("imdbID")
            try:
                det_resp = requests.get(url, params={"i": imdb_id, "apikey": api_key}, timeout=5)
                det = det_resp.json()
                if det.get("Response") == "True":
                    duracion_str = det.get("Runtime", "0").split(" ")[0]
                    duracion = int(duracion_str) if duracion_str.isdigit() else 0
                    clasificacion = det.get("Rated", "") if det.get("Rated") != "N/A" else ""
                    genero = det.get("Genre", "") if det.get("Genre") != "N/A" else ""
                    poster = det.get("Poster", "") if det.get("Poster") != "N/A" else ""
                    
                    resultado.append({
                        "imdb_id": imdb_id,
                        "titulo": det.get("Title", "")[:150],
                        "sinopsis": det.get("Plot", "") if det.get("Plot") != "N/A" else "",
                        "poster_url": poster[:255],
                        "duracion_minutos": duracion,
                        "clasificacion": clasificacion[:10],
                        "genero": genero[:50]
                    })
            except requests.RequestException:
                continue
        
    return resultado

def listar_peliculas(filtros: dict | None = None):
    return peliculas_repo.listar_peliculas(filtros or {})

def obtener_pelicula_por_id(id_pelicula: int):
    return peliculas_repo.obtener_pelicula_por_id(id_pelicula)

def crear_pelicula(datos: dict) -> dict:
    id_nuevo = peliculas_repo.crear_pelicula(datos)
    return {"id": id_nuevo}

def actualizar_pelicula(id_pelicula: int, datos: dict):
    peliculas_repo.actualizar_pelicula(id_pelicula, datos)

def eliminar_pelicula(id_pelicula: int):
    peliculas_repo.eliminar_pelicula(id_pelicula)
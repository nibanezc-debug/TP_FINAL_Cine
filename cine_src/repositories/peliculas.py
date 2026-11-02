from datetime import datetime
from cine_src import db

def _formatear_fila(fila: dict | None) -> dict | None:
    resultado = None
    if fila is not None:
        for campo in ("disponible_desde", "disponible_hasta"):
            if isinstance(fila.get(campo), datetime):
                fila[campo] = fila[campo].strftime("%Y-%m-%d %H:%M:%S")
        if "activa" in fila and fila["activa"] is not None:
            fila["activa"] = bool(fila["activa"])
        resultado = fila
    return resultado

def listar_peliculas(filtros: dict) -> list:
    sql = "SELECT * FROM peliculas WHERE 1=1"
    parametros = []

    if "activa" in filtros:
        sql += " AND activa = %s"
        parametros.append(filtros["activa"])
    else:
        sql += " AND activa = True"

    if "titulo" in filtros:
        sql += " AND titulo LIKE %s"
        parametros.append(f"%{filtros['titulo']}%")

    if "genero" in filtros:
        sql += " AND genero LIKE %s"
        parametros.append(f"%{filtros['genero']}%")

    sql += " ORDER BY id_pelicula DESC"
    filas = db.consultar_todos(sql, tuple(parametros))
    resultado = [_formatear_fila(f) for f in filas]
    return resultado

def obtener_pelicula_por_id(id_pelicula: int):
    sql = "SELECT * FROM peliculas WHERE id_pelicula = %s"
    fila = db.consultar_uno(sql, (id_pelicula,))
    resultado = _formatear_fila(fila)
    return resultado

def crear_pelicula(datos: dict) -> int:
    sql = """
        INSERT INTO peliculas 
        (titulo, sinopsis, poster_url, duracion_minutos, clasificacion, genero, disponible_desde, disponible_hasta, activa) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, True)
    """
    parametros = (
        datos["titulo"], datos["sinopsis"], datos["poster_url"], 
        datos["duracion_minutos"], datos["clasificacion"], datos["genero"], 
        datos["disponible_desde"], datos["disponible_hasta"]
    )
    id_nuevo, _ = db.ejecutar(sql, parametros)
    return id_nuevo

def actualizar_pelicula(id_pelicula: int, datos: dict):
    sql = """
        UPDATE peliculas 
        SET titulo = %s, sinopsis = %s, poster_url = %s, 
            duracion_minutos = %s, clasificacion = %s, genero = %s, 
            disponible_desde = %s, disponible_hasta = %s 
        WHERE id_pelicula = %s
    """
    parametros = (
        datos["titulo"], datos["sinopsis"], datos["poster_url"], 
        datos["duracion_minutos"], datos["clasificacion"], datos["genero"], 
        datos["disponible_desde"], datos["disponible_hasta"], id_pelicula
    )
    db.ejecutar(sql, parametros)

def eliminar_pelicula(id_pelicula: int):
    sql = "UPDATE peliculas SET activa = False WHERE id_pelicula = %s"
    db.ejecutar(sql, (id_pelicula,))
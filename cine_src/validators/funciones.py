from datetime import datetime

from errors import ApiError


def validar_id(valor, nombre: str = "id") -> int:
    if type(valor) is not int or valor <= 0:
        raise ApiError(f"El {nombre} debe ser un entero positivo", 400)
    return valor


def validar_filtros(argumentos) -> dict:
    filtros = {}

    for campo in ("id_pelicula", "id_local", "id_sala"):
        valor = argumentos.get(campo)

        if valor is not None:
            if isinstance(valor, str):
                try:
                    valor = int(valor)
                except ValueError:
                    raise ApiError(
                        f"El filtro {campo} debe ser un entero positivo", 400
                    )

            filtros[campo] = validar_id(valor, campo)

    fecha = argumentos.get("fecha")
    if fecha is not None:
        try:
            fecha_validada = datetime.strptime(fecha, "%Y-%m-%d")
        except (TypeError, ValueError):
            raise ApiError("La fecha debe ser válida y tener formato YYYY-MM-DD", 400)

        filtros["fecha"] = fecha_validada.date().isoformat()

    return filtros


# Campos que pueden enviarse al crear o modificar una función.
CAMPOS_FUNCION = ("id_pelicula", "id_sala", "fecha_hora", "precio")


def validar_datos_funcion(datos, es_patch=False):
    if not isinstance(datos, dict) or not datos:
        raise ApiError("Debés enviar un objeto JSON con datos de la función", 400)

    desconocidos = set(datos) - set(CAMPOS_FUNCION)
    if desconocidos:
        raise ApiError("Hay campos que no corresponden a una función", 400)

    if not es_patch:
        faltantes = [campo for campo in CAMPOS_FUNCION if campo not in datos]
        if faltantes:
            raise ApiError("Faltan campos obligatorios: " + ", ".join(faltantes), 400)

    resultado = {}
    for campo in ("id_pelicula", "id_sala"):
        if campo in datos:
            resultado[campo] = validar_id(datos[campo], campo)

    if "precio" in datos:
        precio = datos["precio"]
        if type(precio) is not int or precio <= 0 or precio > 2147483647:
            raise ApiError("El precio debe ser un entero positivo dentro del rango SQL INT", 400)
        resultado["precio"] = precio

    if "fecha_hora" in datos:
        valor = datos["fecha_hora"]
        if not isinstance(valor, str):
            raise ApiError("La fecha_hora debe ser texto", 400)
        fecha = None
        for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                fecha = datetime.strptime(valor.strip(), formato)
                break
            except ValueError:
                pass
        if fecha is None:
            raise ApiError("fecha_hora debe tener formato YYYY-MM-DD HH:MM:SS", 400)
        resultado["fecha_hora"] = fecha.strftime("%Y-%m-%d %H:%M:%S")

    return resultado

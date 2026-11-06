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

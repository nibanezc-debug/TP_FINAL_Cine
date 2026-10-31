from cine_src.errors import ApiError

def validar_id(numero: int) -> int:
    if type(numero) is not int or numero <= 0:
        raise ApiError('El identificador debe ser un entero positivo', 400)
    return numero

def validar_servicio(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    nombre = datos.get('nombre')
    precio = datos.get('precio')
    if not isinstance(nombre, str) or not nombre.strip() or len(nombre.strip()) > 100:
        raise ApiError('El nombre es obligatorio y debe tener hasta 100 caracteres', 400)
    if type(precio) is not int or precio <= 0 or precio > 2147483647:
        raise ApiError('El precio debe ser un entero positivo dentro del rango SQL INT', 400)
    return {'nombre': nombre.strip(), 'precio': precio}

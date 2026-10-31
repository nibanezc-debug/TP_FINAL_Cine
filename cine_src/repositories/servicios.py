from cine_src.db import consultar_todos, consultar_uno, ejecutar

def listar():
    return consultar_todos('SELECT id, nombre, precio FROM servicios WHERE activo = 1 ORDER BY id')

def buscar(identificador: int):
    return consultar_uno('SELECT id, nombre, precio FROM servicios WHERE id = %s AND activo = 1', (identificador,))

def insertar(nombre: str, precio: int) -> int:
    identificador, _ = ejecutar('INSERT INTO servicios (nombre, precio, activo) VALUES (%s, %s, 1)', (nombre, precio))
    return identificador

def actualizar(identificador: int, nombre: str, precio: int) -> bool:
    _, filas = ejecutar('UPDATE servicios SET nombre = %s, precio = %s WHERE id = %s AND activo = 1', (nombre, precio, identificador))
    return filas > 0

def desactivar(identificador: int) -> bool:
    _, filas = ejecutar('UPDATE servicios SET activo = 0 WHERE id = %s AND activo = 1', (identificador,))
    return filas > 0

from db import consultar_todos, consultar_uno, ejecutar


def listar_locales():
    return consultar_todos("SELECT * FROM locales")


def buscar_local_por_id(id_local):
    return consultar_uno("SELECT * FROM locales WHERE id = %s", (id_local,))

def contar_salas_de_local(id_local):
    resultado = consultar_uno("SELECT COUNT(*) AS total FROM salas WHERE id_local = %s", (id_local,))
    return resultado['total'] if resultado else 0
from cine_src.db import obtener_conexion
from cine_src.errors import ApiError

def crear_usuario(nombre: str, email: str, password: str, rol: str = 'cliente') -> int:
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True) #Devuelve un diccionario donde las claves son los nombres de las columnas en SQL
        try:
            query = """
                INSERT INTO usuarios (nombre, email, password, rol, fecha_registro)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (nombre, email, password, rol))
            conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            if getattr(e, 'errno', None) == 1062: # Error de mail duplicado
                raise ApiError('El correo ya se encuentra registado', 400)
            raise e
        finally:
            cursor.close()

def buscar_por_email(email: str):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "SELECT id, nombre, email, password, rol FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        finally:
            cursor.close()

def buscar_por_id(id_usuario: int):
    with obtener_conexion() as conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                query = "SELECT id, nombre, email, password, rol FROM usuarios WHERE id = %s"
                cursor.execute(query, (id_usuario,))
                return cursor.fetchone()
            finally:
                cursor.close()
                
def listar_todos():
    with obtener_conexion() as conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                query = "SELECT id, nombre, email, password, rol FROM usuarios ORDER BY id ASC"
                cursor.execute(query)
                return cursor.fetchone()
            finally:
                cursor.close()
                
def actualizar_usuario(id_usuario: int, nombre: str, email: str):
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            query = "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s"
            cursor.execute(query, (nombre, email, id_usuario))
            conexion.commit()
        finally:
            cursor.close()
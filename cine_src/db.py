import os
from contextlib import contextmanager
import mysql.connector

@contextmanager
def obtener_conexion():
    conexion = mysql.connector.connect(host=os.getenv('DB_HOST', '127.0.0.1'), port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'root'), password=os.getenv('DB_PASSWORD', ''), database=os.getenv('DB_NAME', 'cine_paradiso'))
    try:
        yield conexion
    finally:
        conexion.close()

def consultar_todos(sql: str, parametros: tuple=()) -> list:
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            cursor.close()

def consultar_uno(sql: str, parametros: tuple=()) -> dict | None:
    with obtener_conexion() as conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchone()
        finally:
            cursor.close()

def ejecutar(sql: str, parametros: tuple=()) -> tuple[int, int]:
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(sql, parametros)
            identificador, filas = (cursor.lastrowid, cursor.rowcount)
            conexion.commit()
            return (identificador, filas)
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()

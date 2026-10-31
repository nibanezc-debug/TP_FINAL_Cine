import getpass
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash
from cine_src.db import ejecutar

def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ('cliente', 'administrador'):
        print('Uso: python -m scripts.crear_usuario_prueba EMAIL cliente|administrador')
        return 1
    email, rol = (sys.argv[1], sys.argv[2])
    password = getpass.getpass('Contraseña para pruebas: ')
    if len(password) < 10:
        print('Elegí al menos 10 caracteres')
        return 1
    identificador, _ = ejecutar('INSERT INTO usuarios (nombre, email, password_hash, rol, fecha_registro) VALUES (%s, %s, %s, %s, %s)', ('Usuario prueba', email, generate_password_hash(password), rol, datetime.now()))
    print('Usuario de prueba creado. ID:', identificador)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

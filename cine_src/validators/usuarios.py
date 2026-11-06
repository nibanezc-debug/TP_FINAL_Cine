from errors import ApiError

def validar_id(valor, nombre: str = 'id_usuario') -> int:
    if type(valor) is not int or valor <= 0:
        raise ApiError(f"El {nombre} debe ser un entero positivo")
    return valor

def validar_registro(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    
    nombre = datos.get('nombre')
    email = datos.get('email')
    password = datos.get('password')
    
    if not isinstance(nombre, str) or not nombre.strip() or len(nombre.strip()) > 100:
        raise ApiError('El nombre es obligatorio y debe tener hasta 100 caracteres', 400)
    
    if not isinstance(email, str) or not email.strip() or '@' not in email or len(email.strip()) > 100:
        raise ApiError('Debe ingresar un correo electrónico válido')
    
    if not isinstance(password, str) or not password:
        raise ApiError('La contraseña es obligatoria', 400)
    
    return {
        'nombre': nombre.strip(),
        'email': email.strip().lower(),
        'password': password
    }

def validar_login(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    
    email = datos.get('email')
    password = datos.get('password')
    
    if not isinstance(email, str) or not email.strip():
        raise ApiError('Debe ingresar un correo electrónico válido')
    
    if not isinstance(password, str) or not password:
        raise ApiError('La contraseña es obligatoria', 400)
    
    return {
        'email': email.strip().lower(),
        'password': password
    }

def validar_actualizacion(datos: dict) -> dict:
    if not isinstance(datos, dict):
        raise ApiError('El cuerpo debe ser un objeto JSON', 400)
    
    resultado = {}
    
    if 'nombre' in datos:
        nombre = datos['nombre']
        if not isinstance(nombre, str) or not nombre.strip() or len(nombre.strip()) >100:
            raise ApiError('El nombre debe ser un texto de hasta 100 caracteres', 400)
        resultado['nombre'] = nombre.strip()
    
    if 'email' in datos:
            email = datos['email']
            if not isinstance(nombre, str) or not email.strip() or '@' not in email or len(email.strip()) >100:
                raise ApiError('El email ingresado no es válido', 400)
            resultado['email'] = email.strip().lower()
        
    if not resultado:
        raise ApiError('No se enviaron campos válidos para actualizar', 400)

    return resultado
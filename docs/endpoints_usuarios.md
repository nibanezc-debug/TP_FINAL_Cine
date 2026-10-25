# Documentación de Endpoints — Módulo de Usuarios

## Especificaciones Generales
* **Formato de datos:** Todos los datos enviados y recibidos se procesan en formato JSON.
* **Seguridad y Roles:** El sistema distingue entre rol `cliente` y `administrador`.

---

### 1. Registro de Usuario
* **Ruta:** `/api/auth/register`
* **Método HTTP:** `POST`
* **Descripción:** Permite el registro de un nuevo cliente en el sistema.
* **Cuerpo de la Petición (Request JSON):**
```json
{
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "password": "Password123"
}
```
* **Respuesta satisfactoria (Código 201 Created):**
```json
{
    "mensaje": "Usuario registrado exitosamente",
    "id_usuario": 1
}
```
* **Respuesta de error(400 Bad Request):**
```json
{
    "error": "Falta completar algún campo o el correo ya se encuentra registrado."
}
```

### 2. Inicio de sesión(Login)
* **Ruta:** `/api/auth/login`
* **Método HTTP:** `POST`
* **Descripción:** Autentica al usuario y devuelve sus datos junto con el rol para definir el acceso en el Frontend/Backoffice.
* **Cuerpo de la Petición (Request JSON):**
```json
{
    "email": "juan@email.com",
    "password": "pepito123"
}
```
**Respuesta satisfactoria (Código 200 OK):**
```json
{
    "id_usuario":1,
    "nombre": "Juan Perez",
    "email": "juan@email.com",
    "rol": "cliente"
}
```
* **Respuesta de error(401 Unauthorized):**
```json
{
    "error": "Contraseña o correo electrónico incorrectos."
}
```

### 3. Obtener Perfil de Usuario
* **Ruta:** `/api/usuarios/<int:id_usuario>`
* **Método HTTP:** `GET`
* **Descripción:** Obtiene el perfil de usuario específico.
* **Respuesta satisfactoria(Código 200 OK):**
```json
{
    "id_usuario": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "rol": "cliente",
    "fecha_registro": "2026-10-24 18:30:00"
}
```

* **Respuesta de error(404 Not Found):**
```json
{
    "error":"El usuario solicitado no existe"
}
```

### 4. Actualizar Datos de Usuario
* **Ruta:** `/api/usuarios/<int:id_usuario>`
* **Método HTTP:** `PUT`
* **Descripción:** Permite al usuario modificar sus datos personales
* **Cuerpo de la Petición (Request JSON):**
```json
{
    "nombre": "Juan Pérez",
    "email": "juan@email.com"
}
```
* **Respuesta satisfactoria(Código 200 OK):**
```json
{
    "mensaje": "Perfil actualizado correctamente"
}
```

* **Respuesta de error(400 Bad Request):**
```json
{
    "error":"Datos inválidos o faltantes"
}
```

### 5. Listar Todos los Usuarios
* **Ruta:** `/api/usuarios`
* **Método HTTP:** `GET`
* **Descripción:** Permite al administrador consultar la lista global de usuarios registrados.

* **Respuesta satisfactoria(Código 200 OK):**
```json
[ 
{
    "id_usuario": 1,
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "rol": "cliente"
},
{
    "id_usuario": 2,
    "nombre": "Admin Cine",
    "email": "admin@cineparadiso.com",
    "rol": "administrador"
}
]
```

* **Respuesta de error(403 Forbidden):**
```json
{
    "error": "Acceso no autorizado para usuarios con rol cliente."
}
```
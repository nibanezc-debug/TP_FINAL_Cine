# Módulo de usuarios - endpoints implementados (Thiago)

| HTTP | Ruta | Permiso | Comportamiento |
|---|---|---|---|
| POST | /api/auth/register | público | Crea un nuevo usuario con rol `cliente`. Recibe JSON: `nombre`, `email`, `password` |
| POST | /api/auth/login | público | Valida credenciales y guarda la sesión (`session['id_usuario']` y `session['rol']`) |
| POST | /api/auth/logout | cliente/admin | Destruye la sesión activa del usuario |
| GET | /api/usuarios/{id} | cliente/admin | Obtiene perfil del usuario (cliente solo ve el suyo, admin ve cualquiera) |
| PUT | /api/usuarios/{id} | cliente/admin | Modifica `nombre` e `email` del usuario autenticado |
| GET | /api/usuarios | admin | Lista todos los usuarios registrados en el sistema |

Autenticación mediante sesión de Flaks (`session['id_usuario']`)
Los roles se comprueban con los datos reales de la base de datos `cine_paradiso`.
El frontend debe comunicarse con el backend mediante la biblioteca Python `requests`.
Crear las tablas ejecutando `bd/schema.sql` en la base `cine_paradiso`.
El campo `email` posee restricción `UNIQUE` para evitar registros duplicados.
# API de Usuarios

Servicio: `users_app` — Base de datos: `users_db`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/users` | Crea un usuario |
| PATCH | `/users/{id}` | Actualiza `status`, `dni`, `fullName`, `phoneNumber` |
| POST | `/users/auth` | Genera un token de sesión |
| GET | `/users/me` | Consulta el usuario dueño del token (`Authorization: Bearer <token>`) |
| GET | `/users/count` | Cuenta usuarios almacenados |
| GET | `/users/ping` | Health check → `pong` |
| POST | `/users/reset` | Elimina todos los usuarios |

Ver contrato completo (cuerpos y códigos de respuesta) en el enunciado de la Entrega 1.

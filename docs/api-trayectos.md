# API de Trayectos

Servicio: `routes_app` — Base de datos: `routes_db`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/routes` | Crea un trayecto (requiere `Authorization`) |
| GET | `/routes?flight={flightId}` | Lista/filtra trayectos (requiere `Authorization`) |
| GET | `/routes/{id}` | Consulta un trayecto (requiere `Authorization`) |
| DELETE | `/routes/{id}` | Elimina un trayecto (requiere `Authorization`) |
| GET | `/routes/count` | Cuenta trayectos almacenados |
| GET | `/routes/ping` | Health check → `pong` |
| POST | `/routes/reset` | Elimina todos los trayectos |

Ver contrato completo (cuerpos y códigos de respuesta) en el enunciado de la Entrega 1.

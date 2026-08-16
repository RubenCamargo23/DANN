# API de Publicaciones

Servicio: `posts_app` — Base de datos: `posts_db`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/posts` | Crea una publicación |
| GET | `/posts?expire={true\|false}&route={routeId}&owner={userId}` | Lista/filtra publicaciones |
| GET | `/posts/{id}` | Consulta una publicación |
| DELETE | `/posts/{id}` | Elimina una publicación |
| GET | `/posts/count` | Cuenta publicaciones almacenadas |
| GET | `/posts/ping` | Health check → `pong` |
| POST | `/posts/reset` | Elimina todas las publicaciones |

Ver contrato completo (cuerpos y códigos de respuesta) en el enunciado de la Entrega 1.

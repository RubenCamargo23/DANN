# API de Ofertas

Servicio: `offers_app` — Base de datos: `offers_db`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/offers` | Crea una oferta |
| GET | `/offers?post={postId}&owner={userId}` | Lista/filtra ofertas |
| GET | `/offers/{id}` | Consulta una oferta |
| DELETE | `/offers/{id}` | Elimina una oferta |
| GET | `/offers/count` | Cuenta ofertas almacenadas |
| GET | `/offers/ping` | Health check → `pong` |
| POST | `/offers/reset` | Elimina todas las ofertas |

Ver contrato completo (cuerpos y códigos de respuesta) en el enunciado de la Entrega 1.

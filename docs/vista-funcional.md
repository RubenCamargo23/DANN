# Vista funcional

Describe los componentes de ejecución que conforman el sistema en esta primera entrega.

## Modelo de componentes

![components](diagrams/components.puml)

## Componentes

| Componente | Responsabilidad | API |
|---|---|---|
| `users_app` | Registro, actualización y autenticación de usuarios | [API de Usuarios](api-usuarios.md) |
| `routes_app` | Gestión de trayectos disponibles para envío | [API de Trayectos](api-trayectos.md) |
| `posts_app` | Gestión de publicaciones sobre trayectos | [API de Publicaciones](api-publicaciones.md) |
| `offers_app` | Gestión de ofertas sobre publicaciones | [API de Ofertas](api-ofertas.md) |

En esta entrega los componentes están completamente desacoplados: ninguno invoca directamente a otro. Cada uno expone su propio API REST y persiste en su propia base de datos PostgreSQL.

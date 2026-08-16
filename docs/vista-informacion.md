# Vista de información

Describe los datos que maneja el sistema. Cada microservicio es dueño exclusivo de su propia información y base de datos; no existe acceso directo entre bases de datos de distintas aplicaciones.

## Glosario

- **Trayecto**: punto de inicio y fin de un viaje, con fecha y costo de envío de una maleta.
- **Publicación**: aviso de disponibilidad para llevar un encargo en un trayecto durante unas fechas específicas.
- **Oferta**: solicitud de un usuario sobre una publicación para enviar un encargo, con descripción, tamaño, fragilidad y monto propuesto.

## Modelo de entidades

![entities](diagrams/entities.puml)

- `User`: gestionada por `users_app` en `users_db`.
- `Route`: gestionada por `routes_app` en `routes_db`.
- `Post`: gestionada por `posts_app` en `posts_db`.
- `Offer`: gestionada por `offers_app` en `offers_db`.

Las referencias entre entidades de distintas bases de datos (por ejemplo `Post.routeId` → `Route.id`) son lógicas, no llaves foráneas físicas, dado que cada base de datos es independiente.

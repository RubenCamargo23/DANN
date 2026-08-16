# Sistema de envío colaborativo de paquetes

Plataforma tipo broker que conecta viajeros con espacio disponible en su maleta (arrendadores) con usuarios que desean enviar paquetes (arrendatarios), bajo un modelo de economía colaborativa.

## Equipo

| Campo | Valor |
|---|---|
| Nombre del grupo | `<nombre del equipo>` |
| Líder del grupo | `<usuario uniandes>` |

| Nombre | Usuario GitHub | Correo Uniandes | Rol actual | Intereses |
|---|---|---|---|---|
| `<nombre>` | `<usuario-github>` | `<usuario>@uniandes.edu.co` | `<rol>` | `<intereses>` |
| `<nombre>` | `<usuario-github>` | `<usuario>@uniandes.edu.co` | `<rol>` | `<intereses>` |
| `<nombre>` | `<usuario-github>` | `<usuario>@uniandes.edu.co` | `<rol>` | `<intereses>` |
| `<nombre>` | `<usuario-github>` | `<usuario>@uniandes.edu.co` | `<rol>` | `<intereses>` |

## Reglas del equipo

1. Cada integrante es dueño de un microservicio y responde por su código, pruebas y despliegue.
2. Todo cambio a `main` se hace por Pull Request con al menos una revisión de otro integrante.
3. El tablero Kanban del repositorio se actualiza antes de cada reunión síncrona semanal.
4. Ningún commit se hace directo sobre `main`; se trabaja en ramas por feature.
5. Cualquier bloqueo se comunica en el canal del equipo dentro de las primeras 24 horas de detectado.

## Tecnologías

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework web | FastAPI |
| Gestión de dependencias | Poetry |
| Pruebas | Pytest + pytest-cov |
| Base de datos | PostgreSQL 15 |
| Contenerización | Docker |
| Orquestación | Kubernetes (Minikube) |
| Documentación | Markdown + PlantUML |

## Vistas de arquitectura

- [Vista de información](vista-informacion.md)
- [Vista funcional](vista-funcional.md)
- [Vista de despliegue](vista-despliegue.md)
- [Vista de desarrollo](vista-desarrollo.md)

## Diagramas

Los diagramas oficiales (exigidos por el enunciado y validados por el pipeline `ci_evaluador_entrega1_docs.yml`) están en PlantUML, en [`diagrams/`](diagrams/): `entities.puml`, `components.puml`, `deployment.puml`, `networks.puml`.

Como material complementario (por ejemplo para el video de sustentación), los mismos 4 diagramas también existen en formato draw.io en [`diagrams/drawio/`](diagrams/drawio/). Para editarlos, importa el `.drawio` correspondiente en [app.diagrams.net](https://app.diagrams.net) (o la app de escritorio draw.io).

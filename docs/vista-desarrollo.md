# Vista de desarrollo

Describe las decisiones de desarrollo tomadas para la construcción del proyecto.

## Estructura de carpetas

```
DANN/
├── users_app/       # Microservicio de usuarios
├── routes_app/      # Microservicio de trayectos
├── posts_app/       # Microservicio de publicaciones
├── offers_app/      # Microservicio de ofertas
├── k8s/             # Manifiestos de Kubernetes
├── docs/            # Documentación técnica (este sitio)
│   └── diagrams/    # Diagramas PlantUML
├── .github/workflows/  # Pipelines de CI
├── makefile         # Reglas usadas por los pipelines evaluadores (no modificar)
└── config.yaml      # Configuración del equipo y de las aplicaciones
```

Cada aplicación es un monorepo-componente independiente: tiene su propio `pyproject.toml`, dependencias, pruebas y `Dockerfile`, y no comparte código con las demás para mantener bajo acoplamiento.

## Arquitectura hexagonal (ports & adapters)

Cada aplicación sigue el mismo patrón dentro de su carpeta `src/`:

```
<app>/src/
├── domain/
│   ├── models/        # Entidades de dominio (Pydantic), sin dependencias de infraestructura
│   ├── ports/          # Interfaces (ABC) que deben cumplir los adaptadores
│   └── use_cases/      # Un caso de uso por operación de negocio
├── adapters/
│   └── database/       # Implementación SQLAlchemy/PostgreSQL de cada port
├── entrypoints/
│   └── api/
│       ├── main.py      # Construcción de la app FastAPI
│       ├── schemas.py   # DTOs de request/response
│       └── routers/     # Rutas HTTP que invocan los use cases
├── assembly.py         # Composition root: cablea qué adapter implementa cada port
├── config.py           # Variables de ambiente centralizadas
└── errors.py           # Excepciones de dominio
```

- Las rutas (`entrypoints`) nunca importan SQLAlchemy directamente: reciben un caso de uso ya ensamblado vía `Depends()`.
- Los casos de uso (`domain/use_cases`) solo conocen el *port* abstracto (`UserRepositoryPort`, `RouteRepositoryPort`, etc.), nunca la base de datos real.
- Los adaptadores (`adapters/database`) traducen entre el modelo de dominio (Pydantic) y el modelo ORM (SQLAlchemy), y son el único lugar que sabe que la persistencia es PostgreSQL.
- `assembly.py` es el único punto donde se decide qué implementación concreta usa cada caso de uso.

Las pruebas unitarias replican esta misma estructura bajo `tests/unit/`, con `conftest.py` por carpeta para fixtures y mocks del repositorio (vía `pytest-mock`).

## Tabla de tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.11 | Lenguaje de desarrollo |
| FastAPI | Framework web / definición de API REST |
| SQLAlchemy | ORM para acceso a PostgreSQL |
| Poetry | Gestión de dependencias y entornos virtuales |
| Pytest + pytest-cov | Pruebas unitarias y cobertura (mínimo 70%) |
| Docker | Contenerización de cada microservicio |
| Minikube + kubectl | Orquestación y despliegue local |
| GitHub Actions | Integración continua (pruebas y documentación) |
| PlantUML | Diagramas de arquitectura como código |
| pytest-mock | Mocks de repositorios en pruebas de casos de uso |

## Convenciones

- Cada base de datos usa el puerto `5432` y corre en su propio contenedor.
- Los identificadores de entidades son `uuid` generados en la aplicación.
- Las fechas se manejan en formato ISO `yyyy-mm-ddTHH:MM:SS` en UTC+0.
- Cada aplicación expone `GET /<recurso>/ping` y `POST /<recurso>/reset` para health-check y limpieza de datos en pruebas.

# routes_app

Microservicio de gestión de trayectos (rutas de viaje usadas por las publicaciones). Implementa arquitectura hexagonal (ports & adapters) con FastAPI, Poetry y PostgreSQL.

## Estructura

```
routes_app/
├── src/
│   ├── domain/
│   │   ├── models/route.py
│   │   ├── ports/route_repository_port.py
│   │   └── use_cases/               # create, get, list, delete, count, reset
│   ├── adapters/database/
│   │   ├── session.py
│   │   ├── route_model.py
│   │   └── route_repository_adapter.py
│   ├── entrypoints/api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── routers/route_router.py
│   ├── assembly.py
│   ├── config.py
│   └── errors.py
├── tests/unit/
├── Dockerfile
└── pyproject.toml
```

## Variables de ambiente

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Password de PostgreSQL | `postgres` |
| `DB_NAME` | Nombre de la base de datos | `routes_db` |

## Ejecución local

```bash
poetry install
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 8000
```

## Pruebas

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

## Docker

```bash
docker build --target runner -t routes_app:latest .
docker run -p 8000:8000 --env-file .env routes_app:latest
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/routes` | Crea un trayecto (requiere `Authorization`) |
| GET | `/routes?flight={flightId}` | Lista/filtra trayectos (requiere `Authorization`) |
| GET | `/routes/{id}` | Consulta un trayecto (requiere `Authorization`) |
| DELETE | `/routes/{id}` | Elimina un trayecto (requiere `Authorization`) |
| GET | `/routes/count` | Cuenta trayectos almacenados |
| GET | `/routes/ping` | Health check |
| POST | `/routes/reset` | Elimina todos los datos |

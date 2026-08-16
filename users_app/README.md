# users_app

Microservicio de gestión de usuarios. Implementa arquitectura hexagonal (ports & adapters) con FastAPI, Poetry y PostgreSQL.

## Estructura

```
users_app/
├── src/
│   ├── domain/
│   │   ├── models/user.py           # Entidad de dominio User (Pydantic)
│   │   ├── ports/user_repository_port.py
│   │   └── use_cases/               # create, update, authenticate, get_authenticated, count, reset
│   ├── adapters/database/
│   │   ├── session.py               # engine/SessionLocal/Base
│   │   ├── user_model.py            # Modelo SQLAlchemy
│   │   └── user_repository_adapter.py
│   ├── entrypoints/api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── routers/user_router.py
│   ├── assembly.py
│   ├── config.py
│   ├── security.py                  # hashing de password y generación de token
│   └── errors.py
├── tests/unit/                      # espeja la estructura de src/
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
| `DB_NAME` | Nombre de la base de datos | `users_db` |

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
docker build --target runner -t users_app:latest .
docker run -p 8000:8000 --env-file .env users_app:latest
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/users` | Crea un usuario |
| PATCH | `/users/{id}` | Actualiza un usuario |
| POST | `/users/auth` | Genera un token de sesión |
| GET | `/users/me` | Consulta el usuario autenticado |
| GET | `/users/count` | Cuenta usuarios almacenados |
| GET | `/users/ping` | Health check |
| POST | `/users/reset` | Elimina todos los datos |

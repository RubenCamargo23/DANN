# posts_app

Microservicio de gestión de publicaciones (avisos de disponibilidad de espacio en maleta para un trayecto). Implementa arquitectura hexagonal (ports & adapters) con FastAPI, Poetry y PostgreSQL.

## Estructura

```
posts_app/
├── src/
│   ├── domain/
│   │   ├── models/post.py
│   │   ├── ports/post_repository_port.py
│   │   └── use_cases/               # create, get, list, delete, count, reset
│   ├── adapters/database/
│   │   ├── session.py
│   │   ├── post_model.py
│   │   └── post_repository_adapter.py
│   ├── entrypoints/api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── routers/post_router.py
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
| `DB_NAME` | Nombre de la base de datos | `posts_db` |

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
docker build --target runner -t posts_app:latest .
docker run -p 8000:8000 --env-file .env posts_app:latest
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/posts` | Crea una publicación |
| GET | `/posts?expire={bool}&route={id}&owner={id}` | Lista/filtra publicaciones |
| GET | `/posts/{id}` | Consulta una publicación |
| DELETE | `/posts/{id}` | Elimina una publicación |
| GET | `/posts/count` | Cuenta publicaciones almacenadas |
| GET | `/posts/ping` | Health check |
| POST | `/posts/reset` | Elimina todos los datos |

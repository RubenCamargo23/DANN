# offers_app

Microservicio de gestión de ofertas sobre publicaciones (solicitudes de envío de un paquete en un trayecto). Implementa arquitectura hexagonal (ports & adapters) con FastAPI, Poetry y PostgreSQL.

## Estructura

```
offers_app/
├── src/
│   ├── domain/
│   │   ├── models/offer.py
│   │   ├── ports/offer_repository_port.py
│   │   └── use_cases/               # create, get, list, delete, count, reset
│   ├── adapters/database/
│   │   ├── session.py
│   │   ├── offer_model.py
│   │   └── offer_repository_adapter.py
│   ├── entrypoints/api/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── routers/offer_router.py
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
| `DB_NAME` | Nombre de la base de datos | `offers_db` |

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
docker build --target runner -t offers_app:latest .
docker run -p 8000:8000 --env-file .env offers_app:latest
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/offers` | Crea una oferta |
| GET | `/offers?post={id}&owner={id}` | Lista/filtra ofertas |
| GET | `/offers/{id}` | Consulta una oferta |
| DELETE | `/offers/{id}` | Elimina una oferta |
| GET | `/offers/count` | Cuenta ofertas almacenadas |
| GET | `/offers/ping` | Health check |
| POST | `/offers/reset` | Elimina todos los datos |

# Proyecto - Desarrollo de Aplicaciones Nativas en la Nube

Sistema de intermediación (broker) para envío colaborativo de paquetes, aprovechando el espacio disponible en la maleta de viajeros.

## Estructura del repositorio

```
.
├── users_app/        # Microservicio de usuarios (código, tests, Dockerfile, README)
├── routes_app/       # Microservicio de trayectos
├── posts_app/        # Microservicio de publicaciones
├── offers_app/       # Microservicio de ofertas
├── k8s/              # Manifiestos de Kubernetes (Deployments, Services, NetworkPolicies)
├── docs/             # Documentación técnica (vistas de arquitectura + diagramas PlantUML)
├── .github/workflows/ # Pipelines de integración continua
└── config.yaml       # Configuración del equipo y de las aplicaciones (usado por los pipelines)
```

## Prerrequisitos

- Docker
- Minikube y kubectl
- Python 3.11 y Poetry (para desarrollo local de cada aplicación)
- Node.js y Newman (opcional, solo para correr las colecciones de Postman por consola)

### Instalación de herramientas (macOS con Homebrew)

Si no tienes alguna de estas herramientas instaladas, así es como se instalaron en el ambiente donde se validó este proyecto:

```bash
# Homebrew (si no lo tienes ya)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Docker Desktop
brew install --cask docker
# Abrir Docker Desktop al menos una vez para que el daemon quede corriendo.

# kubectl + Minikube (kubectl se instala como dependencia de minikube)
brew install minikube

# Node.js (trae npm)
brew install node

# Newman (CLI de Postman para correr colecciones desde terminal)
npm install -g newman

# Python 3.11 y Poetry, si vas a correr una aplicación fuera de Docker
brew install python@3.11
curl -sSL https://install.python-poetry.org | python3 -
```

Verificar que todo quedó instalado:

```bash
docker --version
minikube version
kubectl version --client
node --version
newman --version
poetry --version
```

## Levantar el proyecto localmente con Docker (rápido, sin Minikube)

Forma más rápida de tener las 4 aplicaciones arriba para probarlas con Postman, sin pasar por Kubernetes.

1. Crear una red Docker compartida:
   ```bash
   docker network create dann-net
   ```
2. Construir las 4 imágenes (usa el stage `runner`, multi-stage rootless):
   ```bash
   docker build -t users_app:latest --target runner ./users_app
   docker build -t routes_app:latest --target runner ./routes_app
   docker build -t posts_app:latest --target runner ./posts_app
   docker build -t offers_app:latest --target runner ./offers_app
   ```
3. Levantar una base de datos PostgreSQL por aplicación (mismo puerto interno 5432, sin exponerlo al host ya que solo se necesita entre contenedores):
   ```bash
   for app in users routes posts offers; do
     docker run -d --name ${app}-db --network dann-net \
       -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=${app}_db \
       postgres:15
   done
   ```
4. Levantar las 4 aplicaciones, cada una en un puerto distinto del host:
   ```bash
   docker run -d --name users-app  --network dann-net -e DB_HOST=users-db  -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=users_db  -p 8001:8000 users_app:latest
   docker run -d --name routes-app --network dann-net -e DB_HOST=routes-db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=routes_db -p 8002:8000 routes_app:latest
   docker run -d --name posts-app  --network dann-net -e DB_HOST=posts-db  -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=posts_db  -p 8003:8000 posts_app:latest
   docker run -d --name offers-app --network dann-net -e DB_HOST=offers-db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=offers_db -p 8004:8000 offers_app:latest
   ```
5. Verificar que responden:
   ```bash
   curl http://localhost:8001/users/ping
   curl http://localhost:8002/routes/ping
   curl http://localhost:8003/posts/ping
   curl http://localhost:8004/offers/ping
   ```

| App | URL local |
|---|---|
| users_app | `http://localhost:8001` |
| routes_app | `http://localhost:8002` |
| posts_app | `http://localhost:8003` |
| offers_app | `http://localhost:8004` |

Para detener y limpiar todo:
```bash
for app in users routes posts offers; do docker rm -f ${app}-app ${app}-db; done
docker network rm dann-net
```

## Despliegue completo en Minikube

### Instalar Minikube y kubectl (una sola vez)

```bash
brew install minikube   # instala kubectl como dependencia
```

### Levantar el clúster y desplegar

1. Iniciar Minikube. La entrega exige un mínimo de 4GB RAM y 2 Cores para correr todo localmente, así que se recomienda fijar el clúster a ese límite para detectar problemas de recursos temprano. **El flag `--cni=calico` es obligatorio**: el CNI por defecto de Minikube no implementa `NetworkPolicy`, así que sin Calico las políticas de red se crean pero no bloquean nada (verificado en la práctica, ver [`VALIDACION.md`](VALIDACION.md)):
   ```bash
   minikube start --cpus=2 --memory=4096 --cni=calico
   ```
2. Configurar el shell para usar el daemon de Docker de Minikube (para que las imágenes construidas localmente sean visibles al clúster, sin necesidad de subirlas a un registry):
   ```bash
   eval $(minikube docker-env)
   ```
3. Construir las imágenes de cada aplicación (con el daemon de Minikube ya activo en este shell):
   ```bash
   docker build -t users_app:latest --target runner ./users_app
   docker build -t routes_app:latest --target runner ./routes_app
   docker build -t posts_app:latest --target runner ./posts_app
   docker build -t offers_app:latest --target runner ./offers_app
   ```
4. Aplicar los manifiestos de Kubernetes:
   ```bash
   kubectl apply -f k8s/users.yaml
   kubectl apply -f k8s/routes.yaml
   kubectl apply -f k8s/posts.yaml
   kubectl apply -f k8s/offers.yaml
   ```
5. Verificar que todos los pods estén en estado `Running` (puede tardar unos segundos mientras se descarga la imagen `postgres:15` la primera vez). **Es normal ver 1 o 2 reinicios (`RESTARTS`) en las apps al arrancar**: intentan conectarse a PostgreSQL antes de que el contenedor de base de datos esté listo, Kubernetes las reinicia automáticamente y el siguiente intento sí conecta:
   ```bash
   kubectl get pods
   kubectl get pods --watch   # para ver el progreso en vivo
   ```
6. Verificar que las políticas de red, servicios y deployments se crearon correctamente:
   ```bash
   kubectl get networkpolicy
   kubectl get svc
   kubectl get deployments
   ```
7. Probar los endpoints con `kubectl port-forward` (más simple que `minikube service --url` en macOS con el driver Docker, que requiere un túnel adicional):
   ```bash
   kubectl port-forward svc/users-service 8001:8000 &
   kubectl port-forward svc/routes-service 8002:8000 &
   kubectl port-forward svc/posts-service 8003:8000 &
   kubectl port-forward svc/offers-service 8004:8000 &

   curl http://localhost:8001/users/ping
   curl http://localhost:8002/routes/ping
   curl http://localhost:8003/posts/ping
   curl http://localhost:8004/offers/ping
   ```
   O, alternativamente, con el túnel de Minikube (el Service se llama `<app>-service`, tipo `NodePort`):
   ```bash
   minikube service users-service --url
   minikube service routes-service --url
   minikube service posts-service --url
   minikube service offers-service --url
   ```
8. Actualiza el `baseUrl` de la colección de Postman correspondiente con la URL que te devuelva cada comando.

Para una guía más detallada de validación (incluyendo cómo comprobar que el aislamiento de red entre bases de datos realmente funciona), ver [`VALIDACION.md`](VALIDACION.md).

### Limpiar el clúster

```bash
kubectl delete -f k8s/users.yaml -f k8s/routes.yaml -f k8s/posts.yaml -f k8s/offers.yaml
minikube stop      # o `minikube delete` para borrar el clúster por completo
```

## Ejecución local de una aplicación (sin Docker)

Cada aplicación sigue una arquitectura hexagonal (`src/domain`, `src/adapters`, `src/entrypoints`). Para correrla localmente necesitas una instancia de PostgreSQL disponible (ver `.env.example` de cada app para las variables requeridas):

```bash
cd users_app
cp .env.example .env   # y ajusta DB_HOST/DB_PORT/etc si tu Postgres no está en localhost:5432
poetry install
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 8000
```

## Pruebas

Cada aplicación tiene sus propias pruebas unitarias, o puede usar las reglas del `makefile` en la raíz:

```bash
make unittest DIR=users_app
make unittest DIR=routes_app
make unittest DIR=posts_app
make unittest DIR=offers_app
```

Esto ejecuta `pytest --cov=src --cov-fail-under=70` dentro de cada aplicación.

### Colecciones de Postman

Cada aplicación tiene su colección en `tests/api/`:

| App | Colección | `baseUrl` por defecto |
|---|---|---|
| users_app | [`users_app/tests/api/users.postman_collection.json`](users_app/tests/api/users.postman_collection.json) | `http://localhost:8001` |
| routes_app | [`routes_app/tests/api/routes.postman_collection.json`](routes_app/tests/api/routes.postman_collection.json) | `http://localhost:8002` |
| posts_app | [`posts_app/tests/api/posts.postman_collection.json`](posts_app/tests/api/posts.postman_collection.json) | `http://localhost:8003` |
| offers_app | [`offers_app/tests/api/offers.postman_collection.json`](offers_app/tests/api/offers.postman_collection.json) | `http://localhost:8004` |

Para usarlas: importa el `.json` en Postman, deja **No Environment** seleccionado (para no pisar la variable de colección `baseUrl` con la de otro proyecto), y corre la colección completa con **Run collection**. También se pueden ejecutar por consola con [Newman](https://www.npmjs.com/package/newman):

```bash
newman run users_app/tests/api/users.postman_collection.json
```

## Documentación técnica

La documentación completa (vistas de información, funcional, despliegue y desarrollo) se encuentra en la carpeta [`/docs`](docs/) y se publica como GitHub Pages.

## Equipo

Ver [`docs/README.md`](docs/README.md) para la presentación del equipo y las reglas de trabajo.

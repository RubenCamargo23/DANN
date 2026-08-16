# Validación del proyecto — cómo probar todo

Este documento describe, paso a paso y con los comandos reales, cómo se validó que el proyecto funciona: pruebas unitarias, Docker, despliegue en Kubernetes (Minikube) y colecciones de Postman. Úsalo como checklist antes de crear un release.

## Tabla de contenido

- [1. Prerrequisitos](#1-prerrequisitos)
- [2. Pruebas unitarias por aplicación](#2-pruebas-unitarias-por-aplicación)
- [3. Build y prueba de cada imagen Docker de forma aislada](#3-build-y-prueba-de-cada-imagen-docker-de-forma-aislada)
- [4. Levantar las 4 aplicaciones juntas con Docker](#4-levantar-las-4-aplicaciones-juntas-con-docker)
- [5. Probar el flujo de negocio completo](#5-probar-el-flujo-de-negocio-completo)
- [6. Colecciones de Postman con Newman](#6-colecciones-de-postman-con-newman)
- [7. Despliegue y validación en Minikube (con NetworkPolicy real)](#7-despliegue-y-validación-en-minikube-con-networkpolicy-real)
- [8. Validar el aislamiento de red entre aplicaciones](#8-validar-el-aislamiento-de-red-entre-aplicaciones)
- [9. Limpieza](#9-limpieza)
- [10. Lecciones del pipeline GitFlow + SonarCloud](#10-lecciones-del-pipeline-gitflow--sonarcloud)

## 1. Prerrequisitos

```bash
brew install node          # para newman (pruebas de API)
npm install -g newman
brew install minikube      # instala kubectl como dependencia
```

## 2. Pruebas unitarias por aplicación

Cada app usa pytest + pytest-cov, cobertura mínima 70% (`--cov-fail-under=70`).

```bash
cd users_app
poetry install
PYTHONPATH=$(pwd)/src poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

Repetir para `routes_app`, `posts_app`, `offers_app`, o usar el `makefile` de la raíz:

```bash
make unittest DIR=users_app
make unittest DIR=routes_app
make unittest DIR=posts_app
make unittest DIR=offers_app
```

**Resultado esperado:** 143 pruebas en total (39+35+35+34), cobertura ~97% en cada app.

## 3. Build y prueba de cada imagen Docker de forma aislada

```bash
cd users_app
docker build -t users_app:latest --target runner .

docker network create test-net
docker run -d --name test-db --network test-net \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=users_db \
  postgres:15
sleep 5
docker run -d --name test-app --network test-net \
  -e DB_HOST=test-db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=users_db \
  -p 18080:8000 users_app:latest

curl http://localhost:18080/users/ping
curl -X POST http://localhost:18080/users -H "Content-Type: application/json" \
  -d '{"username":"jdoe","password":"secret123","email":"jdoe@example.com"}'

docker rm -f test-db test-app
docker network rm test-net
```

Repetir el mismo patrón para las otras 3 apps, cambiando el nombre y el puerto.

## 4. Levantar las 4 aplicaciones juntas con Docker

```bash
docker network create dann-net

for app in users routes posts offers; do
  docker build -t ${app}_app:latest --target runner ./${app}_app
done

for app in users routes posts offers; do
  docker run -d --name ${app}-db --network dann-net \
    -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=${app}_db \
    postgres:15
done
sleep 6

docker run -d --name users-app  --network dann-net -e DB_HOST=users-db  -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=users_db  -p 8001:8000 users_app:latest
docker run -d --name routes-app --network dann-net -e DB_HOST=routes-db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=routes_db -p 8002:8000 routes_app:latest
docker run -d --name posts-app  --network dann-net -e DB_HOST=posts-db  -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=posts_db  -p 8003:8000 posts_app:latest
docker run -d --name offers-app --network dann-net -e DB_HOST=offers-db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=offers_db -p 8004:8000 offers_app:latest

curl http://localhost:8001/users/ping
curl http://localhost:8002/routes/ping
curl http://localhost:8003/posts/ping
curl http://localhost:8004/offers/ping
```

## 5. Probar el flujo de negocio completo

Crear un usuario, un trayecto, una publicación y una oferta encadenados (usando los ids reales de cada respuesta):

```bash
USER_RESP=$(curl -s -X POST http://localhost:8001/users -H "Content-Type: application/json" \
  -d '{"username":"traveler1","password":"secret123","email":"traveler1@example.com"}')
USER_ID=$(echo $USER_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

ROUTE_RESP=$(curl -s -X POST http://localhost:8002/routes -H "Content-Type: application/json" \
  -H "Authorization: Bearer some-token" -d '{
    "flightId": "AA001", "sourceAirportCode": "BOG", "sourceCountry": "Colombia",
    "destinyAirportCode": "MIA", "destinyCountry": "USA", "bagCost": 50,
    "plannedStartDate": "2027-01-01T10:00:00", "plannedEndDate": "2027-01-01T15:00:00"
  }')
ROUTE_ID=$(echo $ROUTE_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

POST_RESP=$(curl -s -X POST http://localhost:8003/posts -H "Content-Type: application/json" \
  -d "{\"routeId\": \"$ROUTE_ID\", \"expireAt\": \"2026-12-01T10:00:00\", \"userId\": \"$USER_ID\"}")
POST_ID=$(echo $POST_RESP | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

curl -s -X POST http://localhost:8004/offers -H "Content-Type: application/json" \
  -d "{\"postId\": \"$POST_ID\", \"userId\": \"$USER_ID\", \"description\": \"Zapatos\", \"size\": \"MEDIUM\", \"fragile\": false, \"offer\": 45.5}"
```

**Resultado esperado:** cada paso devuelve `201` con un `id` nuevo; el flujo completo no debe fallar en ningún paso.

## 6. Colecciones de Postman con Newman

Con las 4 apps corriendo (puertos 8001-8004, ver sección 4):

```bash
newman run users_app/tests/api/users.postman_collection.json
newman run routes_app/tests/api/routes.postman_collection.json
newman run posts_app/tests/api/posts.postman_collection.json
newman run offers_app/tests/api/offers.postman_collection.json
```

**Resultado esperado:** 0 failures en las 4 colecciones (67 aserciones en total).

## 7. Despliegue y validación en Minikube (con NetworkPolicy real)

**Importante:** el driver por defecto de Minikube usa un CNI que **no aplica** `NetworkPolicy`. Si no se levanta el clúster con `--cni=calico`, las políticas de red se crean sin error pero no bloquean nada — es un falso positivo que hay que evitar.

```bash
minikube start --cpus=2 --memory=4096 --cni=calico
eval $(minikube docker-env)

for app in users routes posts offers; do
  docker build -t ${app}_app:latest --target runner ./${app}_app
done

kubectl apply -f k8s/users.yaml
kubectl apply -f k8s/routes.yaml
kubectl apply -f k8s/posts.yaml
kubectl apply -f k8s/offers.yaml

kubectl get pods --watch   # esperar hasta que los 8 pods estén 1/1 Running
```

**Nota sobre reinicios esperados al arrancar:** las apps pueden fallar 1-2 veces al iniciar (`Error`, `RESTARTS: 1` o `2`) porque intentan conectarse a PostgreSQL antes de que el contenedor de base de datos esté listo para aceptar conexiones. Kubernetes las reinicia automáticamente y el segundo/tercer intento sí conecta. Esto es comportamiento esperado sin un `initContainer` de espera — no es un bug del código de la aplicación.

Verificar que todo quedó saludable:

```bash
kubectl get pods
kubectl get svc
kubectl get networkpolicy
kubectl get deployments
```

Probar los endpoints vía `port-forward` (más simple que `minikube service --url` en macOS con driver Docker, que requiere un túnel adicional):

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

O, alternativamente, usando el túnel de Minikube:

```bash
minikube service users-service --url
minikube service routes-service --url
minikube service posts-service --url
minikube service offers-service --url
```

## 8. Validar el aislamiento de red entre aplicaciones

> **Hallazgo real de esta validación:** al desplegar por primera vez en Minikube **sin** `--cni=calico`, las 4 `NetworkPolicy` se creaban sin error (`kubectl get networkpolicy` las mostraba normales) pero **no bloqueaban nada** — cualquier app podía conectarse a la base de datos de cualquier otra. El CNI por defecto de Minikube no implementa `NetworkPolicy`. Al recrear el clúster con `--cni=calico` (sección 7), las políticas sí bloquean el tráfico cruzado como se esperaba. **Si vas a demostrar el aislamiento de red en el video de sustentación, asegúrate de haber iniciado Minikube con `--cni=calico`, o la demo mostrará que el aislamiento no funciona.**

Cada `NetworkPolicy` debe permitir tráfico a `<app>-db` únicamente desde su propia aplicación. Para comprobarlo, se intenta conectar desde una app que **no** debería tener acceso:

```bash
kubectl exec deploy/offers-app -- python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect(('users-db', 5432))
    print('CONEXION EXITOSA - la network policy NO esta bloqueando (mal)')
except Exception as e:
    print(f'CONEXION BLOQUEADA (correcto): {e}')
"
```

**Resultado esperado:** `CONEXION BLOQUEADA` — si en cambio dice `CONEXION EXITOSA`, revisar que el clúster tenga un CNI compatible con `NetworkPolicy` (Calico) y que las políticas se hayan aplicado correctamente.

Como control, la misma prueba debe **conectar exitosamente** desde la app dueña:

```bash
kubectl exec deploy/users-app -- python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('users-db', 5432))
print('CONEXION EXITOSA (correcto, es la app dueña)')
"
```

## 9. Limpieza

```bash
# Docker suelto (sección 4)
for app in users routes posts offers; do docker rm -f ${app}-app ${app}-db; done
docker network rm dann-net

# Minikube
kubectl delete -f k8s/users.yaml -f k8s/routes.yaml -f k8s/posts.yaml -f k8s/offers.yaml
minikube stop
# o para borrar el clúster por completo:
minikube delete
```

## 10. Lecciones del pipeline GitFlow + SonarCloud

Al construir el flujo automático de release (`develop` → pruebas → `release/X.Y.Z` → PR → merge a `main` → tag → análisis → sync de `develop`), aparecieron varios problemas reales que vale la pena conocer si se modifica el workflow:

- **SonarCloud Free no permite consultar el Quality Gate en ramas distintas a la principal.** Intentar bloquear el release con el resultado del Quality Gate de `develop` falla con `403` (`"Organization is not allowed to access data from non main branches"`). Por eso el análisis se movió a correr sobre `main`, después del merge, y ya no bloquea el release (es informativo).
- **Loop infinito de releases.** El paso que sincroniza `develop` con `main` (`git push origin develop`) vuelve a disparar el trigger `on.push` del propio workflow, generando un release nuevo, cuyo merge sincroniza `develop` de nuevo, en un ciclo sin fin. Se corrigió agregando una condición al job `release-develop` que ignora los push cuyo mensaje de commit empiece con `"chore: sync develop with main"` (usar `contains()` con un texto genérico como `github-actions[bot]` es frágil: cualquier commit que *hable* sobre el bot en su descripción activa el bloqueo por accidente).
- **Renombrar la Main Branch en SonarCloud no reprocesa el historial.** Si el proyecto se creó cuando la rama principal aún se llamaba `master`, renombrarla a `main` desde la configuración del proyecto deja el análisis "congelado" en el commit del rename — los scans posteriores exitosos no logran actualizarlo. La solución que funcionó fue borrar el proyecto en SonarCloud y crearlo de nuevo desde cero (nuevo `SONAR_TOKEN`, actualizado como secret `SONAR_TOKEN` en GitHub).

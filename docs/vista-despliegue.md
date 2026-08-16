# Vista de despliegue

Describe cómo se despliegan los componentes de la vista funcional y sus conectores.

## Modelo de despliegue

![deployment](diagrams/deployment.puml)

Cada aplicación y su base de datos se ejecutan en pods independientes dentro del clúster de Minikube, en el namespace `default`. Las bases de datos usan volúmenes `emptyDir` (efímeros) para tolerar la indisponibilidad momentánea del contenedor sin perder los datos durante la vida del pod.

## Modelo de red

![networks](diagrams/networks.puml)

- Cada aplicación tiene una `NetworkPolicy` asociada a su base de datos que solo permite tráfico entrante desde su propia aplicación, por el puerto `5432`.
- Los `Service` de las bases de datos son de tipo `ClusterIP` (solo accesibles dentro del clúster).
- Los `Service` de las aplicaciones son de tipo `NodePort` (accesibles desde fuera del clúster para pruebas de API).

## Manifiestos

Los archivos de despliegue se encuentran en la carpeta [`/k8s`](../k8s/):

| Archivo | Contenido |
|---|---|
| `k8s/users.yaml` | Deployment/Service de `users-db`, NetworkPolicy, Deployment/Service de `users-app` |
| `k8s/routes.yaml` | Deployment/Service de `routes-db`, NetworkPolicy, Deployment/Service de `routes-app` |
| `k8s/posts.yaml` | Deployment/Service de `posts-db`, NetworkPolicy, Deployment/Service de `posts-app` |
| `k8s/offers.yaml` | Deployment/Service de `offers-db`, NetworkPolicy, Deployment/Service de `offers-app` |

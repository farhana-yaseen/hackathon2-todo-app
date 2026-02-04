# Todo App - Kubernetes Deployment Guide

This guide explains how to deploy the Todo application to a local Kubernetes cluster using Minikube and Helm.

## Prerequisites

- Docker Desktop
- Minikube
- Helm
- kubectl

## Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

### 2. Deploy the Application

You can deploy the application using the helper script:

```bash
./deploy-local.sh
```

Or manually:

1. Set Docker environment to use Minikube's Docker daemon:
   ```bash
   eval $(minikube docker-env)
   ```

2. Build Docker images:
   ```bash
   cd backend
   docker build -t backend:v1 .
   cd ../frontend
   docker build -t frontend:v1 .
   cd ..
   ```

3. Install the Helm chart:
   ```bash
   helm upgrade --install todo-app ./charts/todo-app
   ```

### 3. Access the Application

Once deployed, get the URL for the frontend service:

```bash
minikube service frontend-service
```

Or get just the URL:

```bash
minikube service frontend-service --url
```

## Configuration

The Helm chart can be customized using values in `charts/todo-app/values.yaml`:

- `backend.replicaCount` - Number of backend replicas (default: 1)
- `frontend.replicaCount` - Number of frontend replicas (default: 2)
- `backend.resources` - Resource requests and limits for backend
- `frontend.resources` - Resource requests and limits for frontend
- `secrets` - Secret values for database URL, API keys, etc.

## Scaling

The application includes Horizontal Pod Autoscalers (HPA) for both frontend and backend services. They are configured to scale based on CPU utilization (70% threshold).

To check HPA status:

```bash
kubectl get hpa
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods
```

### Check Logs
```bash
kubectl logs -l app.kubernetes.io/component=backend
kubectl logs -l app.kubernetes.io/component=frontend
```

### Check Services
```bash
kubectl get svc
```

### Check Deployments
```bash
kubectl get deployments
```

### Debug Helm Template
```bash
helm template todo-app ./charts/todo-app
```

## Cleanup

To uninstall the application:

```bash
helm uninstall todo-app
```

To stop Minikube:

```bash
minikube stop
```
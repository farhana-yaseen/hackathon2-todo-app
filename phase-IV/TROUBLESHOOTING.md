# Troubleshooting Guide: Todo App Kubernetes Deployment

This guide covers common issues and solutions when deploying the Todo application to Kubernetes.

## Common Issues

### 1. Images Not Found
**Problem**: Pods stuck in `ImagePullBackOff` state
**Solution**: Ensure you've run `eval $(minikube docker-env)` before building images

### 2. Minikube Not Running
**Problem**: Helm install fails with connection errors
**Solution**: Start Minikube first: `minikube start`

### 3. Insufficient Resources
**Problem**: Pods stuck in `Pending` state
**Solution**: Increase Minikube resources:
```bash
minikube stop
minikube start --memory=4096 --cpus=4
```

### 4. Frontend Cannot Connect to Backend
**Problem**: Cross-origin errors or connection timeouts
**Solution**: Verify that:
- Backend service is named `backend-service`
- Frontend uses the correct service URL (`http://backend-service:8000`)
- CORS is configured to allow all origins in the backend

### 5. Secret Values Not Set
**Problem**: Backend crashes due to missing database URL or API keys
**Solution**: Update values.yaml with your secret values:
```yaml
secrets:
  databaseUrl: "your-db-url-here"
  cohereApiKey: "your-cohere-key-here"
  betterAuthSecret: "your-auth-secret-here"
```

### 6. Port Already Allocated (NodePort)
**Problem**: Service fails to allocate NodePort
**Solution**: Minikube may have limited port range. Check available ports:
```bash
minikube service list
```

## Diagnostic Commands

### Check All Resources
```bash
kubectl get all
```

### Check Specific Pod Logs
```bash
kubectl logs <pod-name>
```

### Check Events
```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Port Forward for Testing
```bash
kubectl port-forward svc/backend-service 8000:8000
kubectl port-forward svc/frontend-service 3000:3000
```

### Describe Resources for Details
```bash
kubectl describe pod <pod-name>
kubectl describe service <service-name>
kubectl describe deployment <deployment-name>
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods -l app.kubernetes.io/name=todo-app
```

### 2. Check Service Status
```bash
kubectl get svc -l app.kubernetes.io/name=todo-app
```

### 3. Check Deployment Status
```bash
kubectl rollout status deployment/todo-app-backend
kubectl rollout status deployment/todo-app-frontend
```

### 4. Test Internal Service Communication
Exec into a frontend pod and test connectivity:
```bash
kubectl exec -it <frontend-pod-name> -- sh
wget -qO- http://backend-service:8000/docs
```

## Reset and Redeploy

If you need to start fresh:

```bash
helm uninstall todo-app
helm install todo-app ./charts/todo-app
```

Or to completely reset:

```bash
helm uninstall todo-app
kubectl delete pvc --all
kubectl delete secrets --selector app.kubernetes.io/name=todo-app
```

## Development Tips

### Hot Reload in Development
For development, you might want to temporarily disable HPA:
```bash
helm upgrade --install todo-app ./charts/todo-app --set backend.hpa.enabled=false --set frontend.hpa.enabled=false
```

### Override Replica Counts
For development, you might want single replicas:
```bash
helm upgrade --install todo-app ./charts/todo-app --set backend.replicaCount=1 --set frontend.replicaCount=1
```

### Enable Debug Logging
Add environment variables for debugging:
```bash
helm upgrade --install todo-app ./charts/todo-app --set backend.additionalEnv.DEBUG=true
```
#!/bin/bash

# Production Deployment Script for Todo App
# This script prepares and deploys the application to a production Kubernetes cluster

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting Production Deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed or not in PATH"
    exit 1
fi

# Check if we're connected to a production cluster (basic check)
CLUSTER_INFO=$(kubectl cluster-info 2>&1)
if [[ $CLUSTER_INFO == *"minikube"* ]]; then
    echo "⚠️  WARNING: You appear to be connected to a minikube cluster, not production!"
    echo "⚠️  This script is intended for production deployment."
    read -p "Are you sure you want to continue? (yes/no): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Deployment cancelled by user"
        exit 1
    fi
fi

echo "✅ Prerequisites verified"

# Check for production secrets
echo "🔍 Verifying production secrets..."
if ! kubectl get secret todo-app-secrets &> /dev/null; then
    echo "❌ Production secrets not found!"
    echo "Please create production secrets before running this script:"
    echo "kubectl create secret generic todo-app-secrets \\"
    echo "  --from-literal=DATABASE_URL='<your-db-url>' \\"
    echo "  --from-literal=COHERE_API_KEY='<your-cohere-key>' \\"
    echo "  --from-literal=BETTER_AUTH_SECRET='<your-auth-secret>'"
    exit 1
else
    echo "✅ Production secrets found"
fi

# Check for production Docker images
echo "🔍 Verifying production Docker images..."
if [[ -z "$IMAGE_TAG" ]]; then
    IMAGE_TAG="prod-$(date +%Y%m%d-%H%M%S)"
    echo "ℹ️  Using auto-generated image tag: $IMAGE_TAG"
fi

# Build and push images to registry (assuming Docker registry is configured)
echo "📦 Building and tagging production images..."
docker build -t todo-backend:$IMAGE_TAG -f backend/Dockerfile backend/
docker build -t todo-frontend:$IMAGE_TAG -f frontend/Dockerfile frontend/

echo "📤 Pushing images to registry..."
# Uncomment the following lines when you have a production registry
# docker tag todo-backend:$IMAGE_TAG your-registry/todo-backend:$IMAGE_TAG
# docker tag todo-frontend:$IMAGE_TAG your-registry/todo-frontend:$IMAGE_TAG
# docker push your-registry/todo-backend:$IMAGE_TAG
# docker push your-registry/todo-frontend:$IMAGE_TAG

# Update values-prod.yaml with the correct image tags
echo "📝 Updating production values with image tags..."
sed -i "s/tag: v1/tag: $IMAGE_TAG/g" charts/todo-app/values-prod.yaml

echo "🔄 Upgrading production deployment..."
helm upgrade --install todo-app-prod ./charts/todo-app \
    --values ./charts/todo-app/values-prod.yaml \
    --namespace production \
    --create-namespace \
    --timeout 10m

echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n production --timeout=300s

echo "✅ Production deployment completed successfully!"

echo "📋 Deployment verification commands:"
echo "   kubectl get pods -n production"
echo "   kubectl get svc -n production"
echo "   kubectl get deployments -n production"
echo "   kubectl logs -l app.kubernetes.io/name=todo-app -n production"

# Get the external IP if using LoadBalancer
echo "🌐 Service endpoints:"
kubectl get svc -n production

echo ""
echo "🎉 Production deployment is now live!"
echo "Remember to monitor the application and set up alerts for production!"
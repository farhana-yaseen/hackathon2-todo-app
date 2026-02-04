#!/bin/bash

# Deployment script for local Kubernetes (Minikube) environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting deployment to local Kubernetes cluster..."

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "⚠️  Minikube is not running. Starting minikube..."
    minikube start
fi

# Set Docker environment to use Minikube's Docker daemon
echo "🐳 Setting up Minikube Docker environment..."
eval $(minikube docker-env)

# Build backend image
echo "🏗️  Building backend Docker image..."
cd backend
docker build -t backend:v1 .
cd ..

# Build frontend image
echo "🏗️  Building frontend Docker image..."
cd frontend
docker build -t frontend:v1 .
cd ..

# Go back to root and deploy with Helm
echo "⎈ Installing/upgrading Helm chart..."
helm upgrade --install todo-app ./charts/todo-app --values ./charts/todo-app/values.yaml

# Wait a moment for the deployment to start
sleep 10

# Check the status of pods
echo "🔍 Checking pod status..."
kubectl get pods

# Show the services
echo "🌐 Services created:"
kubectl get svc

# Show the deployment status
echo "📊 Deployment status:"
kubectl get deployments

# Get the frontend service URL
FRONTEND_URL=$(minikube service frontend-service --url)
echo "🎉 Frontend is available at: $FRONTEND_URL"

echo "✅ Deployment completed successfully!"
echo "💡 To access the application, visit: $FRONTEND_URL"
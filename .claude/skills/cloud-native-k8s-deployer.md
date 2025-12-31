name: "cloud-native-k8s-deployer"
description: "Containerizes the stack and generates Kubernetes manifests. Uses Helm and Docker to prepare the Todo app for local and cloud production."
version: "1.0.0"
---
# How This Skill Works
1. Generates optimized multi-stage `Dockerfiles` for Next.js and FastAPI.
2. Creates a `docker-compose.yml` for local testing.
3. Builds a Helm Chart structure (`/charts`) including deployments, services, and ingresses.
4. Configures `kubectl-ai` or `kagent` commands to automate cluster health checks.
5. Sets up Horizontal Pod Autoscaling (HPA) for the backend API.

# Deliverables
- Dockerfiles (Frontend & Backend)
- Helm Charts (Values.yaml, Templates/)
- Minikube startup script.
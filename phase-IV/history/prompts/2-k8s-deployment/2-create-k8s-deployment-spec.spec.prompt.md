---
id: 2
title: "Create K8s Deployment Spec"
stage: "spec"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "k8s-deployment"
branch: "main"
user: "user"
command: "/sp.specify"
labels: ["spec", "kubernetes", "deployment", "containerization"]
links:
  spec: "./specs/2-k8s-deployment/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/2-k8s-deployment/spec.md"
  - "specs/2-k8s-deployment/checklists/requirements.md"
tests_yaml: []
---

# Prompt Text

```
# Specification: Phase IV - Local Kubernetes Deployment

## 1. Objective
Transform the existing Todo App (Phase III) into a cloud-native application by containerizing the components and orchestrating them using Kubernetes (Minikube) and Helm.

## 2. Component Breakdown

### A. Backend Containerization (FastAPI)
- **Base Image:** `python:3.13-slim`
- **Build Process:**
    - Install system dependencies for PostgreSQL (libpq-dev).
    - Use `pip install` for dependencies.
    - Copy source code and `chat_logic.py`.
- **Runtime:** Expose port `8000`.
- **Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`

### B. Frontend Containerization (Next.js)
- **Base Image:** `node:20-alpine`
- **Build Process:**
    - Multi-stage build (Build stage + Runner stage).
    - `npm install` and `npm run build`.
- **Runtime:** Expose port `3000`.
- **Command:** `npm start`

### C. Orchestration (Helm Chart)
- **Chart Name:** `todo-app`
- **Structure:**
    - `/charts/backend`: Deployment, Service (ClusterIP), HPA.
    - `/charts/frontend`: Deployment, Service (NodePort/LoadBalancer).
- **Replica Counts:**
    - Frontend: 2 replicas (for high availability).
    - Backend: 1 replica (standard).

## 3. Infrastructure Requirements

### Kubernetes Resources
- **Namespaces:** Use `default` or create `todo-namespace`.
- **Secrets:**
    - `todo-secrets`: Encrypt `DATABASE_URL`, `COHERE_API_KEY`, and `BETTER_AUTH_SECRET`.
- **ConfigMaps:**
    - `todo-config`: Store `NEXT_PUBLIC_API_URL` (pointing to the internal backend service).

### Networking
- **Backend Service:** Internal name `backend-service` on port `8000`.
- **Frontend Service:** Accessible via Minikube tunnel or NodePort on port `3000`.
- **Cross-Origin:** Ensure the backend CORS configuration allows the frontend's cluster-internal or external URL.

## 4. Acceptance Criteria
1. **Container Images:** Docker images for both services must build without errors and be optimized for size.
2. **Helm Deployment:** Running `helm install todo-app ./charts` must successfully deploy
```

# Response Text

Created the Phase IV Kubernetes Deployment specification at specs/2-k8s-deployment/spec.md. The specification includes:

- Clear objective for transforming the Todo App into a cloud-native application
- User scenarios covering developer and ops perspectives
- Five functional requirements covering containerization, orchestration, configuration management, and networking
- Non-functional requirements for scalability, availability, and security
- Measurable success criteria with both quantitative and qualitative measures
- Key entities including container images, Kubernetes resources, and Helm components
- Clear scope definition with in/out of scope items
- Dependencies, assumptions, and constraints

Also created the quality checklist at specs/2-k8s-deployment/checklists/requirements.md to validate the specification completeness.

# Outcome

Successfully created a comprehensive specification for the Kubernetes deployment of the Todo application that follows cloud-native principles and meets the requirements for Phase IV transformation.
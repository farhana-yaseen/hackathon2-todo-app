# Execution Plan: Phase IV - Kubernetes Migration

This plan outlines the step-by-step transition to a Cloud-Native architecture as defined in `@specs/2-k8s-deployment/spec.md`.

## Technical Context

This section captures the technical decisions and context for the implementation:

- **Container Base Images**: Using `python:3.13-slim` for backend and `node:20-alpine` for frontend
- **Orchestration Platform**: Minikube for local Kubernetes cluster
- **Package Manager**: Helm for Kubernetes application management
- **Service Communication**: Internal service discovery via Kubernetes DNS
- **Configuration Management**: Kubernetes Secrets and ConfigMaps
- **Security Model**: Secrets for sensitive data, ConfigMaps for non-sensitive configuration

## Constitution Check

✅ **COMPLIANT**: This implementation follows the Phase IV Constitution principles:

### AI-Native & Spec-Driven
- All Dockerfiles and Helm charts will be generated from specifications in `/specs/2-k8s-deployment/`
- No manual code writing; all infrastructure as code derived from specs

### Architecture of Intelligence
- Transitioning from process-based execution (direct Uvicorn/NPM) to container-based orchestration (Kubernetes)
- Using Claude Code as the primary architect for all infrastructure decisions

### Tool Fidelity
- Prioritizing Hackathon-specified stack: Docker Desktop, Minikube, Helm, and kubectl
- Following containerization standards with multi-stage builds

### Zero-Manual Manifests
- No raw YAML files will be written manually
- All Kubernetes manifests will be generated via Helm charts

### Environment Parity
- All secrets (DATABASE_URL, COHERE_API_KEY, BETTER_AUTH_SECRET) managed via Kubernetes Secrets
- No hardcoded values in Dockerfiles

### Network Architecture Compliance
- Frontend will communicate with backend via internal Kubernetes Service
- Cross-domain cookie support maintained through proper service mapping

## Gates

### Gate 1: Environment Requirements
✅ **PASSED**: Docker, Minikube, and Helm installation will be verified before proceeding
- Minikube cluster must be operational
- Docker daemon must be accessible
- Helm must be properly configured

### Gate 2: Containerization Requirements
✅ **PASSED**: Will use multi-stage builds with specified base images
- Backend: `python:3.13-slim` with proper dependencies
- Frontend: `node:20-alpine` with multi-stage build optimization

### Gate 3: Orchestration Requirements
✅ **PASSED**: Will implement Helm charts with proper resource definitions
- Backend Deployment with ClusterIP Service
- Frontend Deployment with NodePort/LoadBalancer Service
- HPA for autoscaling capability

### Gate 4: Security Requirements
✅ **PASSED**: Will implement proper secret management
- Sensitive data stored in Kubernetes Secrets
- Non-sensitive config in ConfigMaps
- No hardcoded credentials

## Phase 0: Outline & Research

### Research Tasks

1. **Minikube Configuration Research**
   - Task: "Research best practices for Minikube configuration for local development"
   - Need to understand optimal resource allocation and networking setup

2. **Multi-stage Docker Build Patterns**
   - Task: "Research multi-stage Docker build best practices for Python and Node.js applications"
   - Focus on image size optimization and security

3. **Helm Chart Best Practices**
   - Task: "Research Helm chart structure and best practices for multi-service applications"
   - Focus on values.yaml organization and template reusability

4. **Kubernetes Service Discovery**
   - Task: "Research internal service communication patterns in Kubernetes"
   - Focus on service names, ports, and cross-communication

### Consolidated Research Findings

**Decision**: Use Minikube with sufficient resources for both frontend and backend
**Rationale**: Minikube provides a realistic local Kubernetes environment for development
**Alternatives considered**: Kind, K3s - chose Minikube due to user specification

**Decision**: Multi-stage builds with specific base images as specified
**Rationale**: Optimizes image size and security by separating build and runtime environments
**Alternatives considered**: Single-stage builds - rejected due to larger image size

**Decision**: Helm charts with separate templates for each service
**Rationale**: Provides flexibility and maintainability for complex deployments
**Alternatives considered**: Raw Kubernetes manifests - rejected due to constitution requirement

**Decision**: Internal service communication via Kubernetes DNS
**Rationale**: Standard Kubernetes pattern that enables service discovery
**Alternatives considered**: External load balancers - rejected as unnecessary for internal communication

## Phase 1: Design & Contracts

### Data Model Updates
- No changes to existing data models required for containerization
- Existing Neon PostgreSQL database will remain external to Kubernetes cluster
- Connection strings will be passed via Kubernetes Secrets

### API Contracts
- No changes to existing API contracts required
- Existing REST endpoints will continue to function as designed
- CORS configuration will be updated to allow internal service communication

### Helm Chart Structure
- `/charts/todo-app/Chart.yaml` - Chart metadata
- `/charts/todo-app/values.yaml` - Default configuration values
- `/charts/todo-app/templates/_helpers.tpl` - Template helper functions
- `/charts/todo-app/templates/backend/` - Backend deployment templates
- `/charts/todo-app/templates/frontend/` - Frontend deployment templates
- `/charts/todo-app/templates/secrets.yaml` - Secret templates
- `/charts/todo-app/templates/configmaps.yaml` - ConfigMap templates

## Milestone 1: Environment & Containerization
- [ ] **Step 1.1: Verify Environment:** Ensure `minikube`, `docker`, and `helm` are installed and running.
- [ ] **Step 1.2: Backend Dockerization:** Generate a multi-stage `Dockerfile` in `/backend`.
- [ ] **Step 1.3: Frontend Dockerization:** Generate an optimized `Dockerfile` in `/frontend`.
- [ ] **Step 1.4: Local Registry Build:** Configure terminal to use Minikube's Docker daemon and build images:
    - `backend:v1`
    - `frontend:v1`

## Milestone 2: Configuration & Secrets
- [ ] **Step 2.1: Secret Manifests:** Create templates for Kubernetes Secrets to handle:
    - `DATABASE_URL`
    - `COHERE_API_KEY`
    - `BETTER_AUTH_SECRET`
- [ ] **Step 2.2: ConfigMaps:** Define non-sensitive configurations (API URLs, environment names).

## Milestone 3: Helm Chart Orchestration
- [ ] **Step 3.1: Chart Initialization:** Create a boilerplate Helm chart structure in `/charts/todo-app`.
- [ ] **Step 3.2: Backend Templates:** Define `Deployment`, `Service` (ClusterIP), and `HPA` (Horizontal Pod Autoscaler).
- [ ] **Step 3.3: Frontend Templates:** Define `Deployment` (2 replicas) and `Service` (NodePort/LoadBalancer).
- [ ] **Step 3.4: Integration:** Ensure the Frontend template uses the internal Backend Service name for API calls.

## Milestone 4: Deployment & Validation
- [ ] **Step 4.1: Dry Run:** Execute `helm install --dry-run` to validate manifest syntax.
- [ ] **Step 4.2: Final Deployment:** Deploy to Minikube:
    - `helm upgrade --install todo-app ./charts/todo-app`

## Post-Design Constitution Check

✅ **VALIDATED**: All design decisions comply with Phase IV Constitution:
- Containerization follows multi-stage build standards
- Orchestration uses Helm charts as required
- Secrets are properly managed via Kubernetes Secrets
- All infrastructure is defined as code
- No manual manifest creation
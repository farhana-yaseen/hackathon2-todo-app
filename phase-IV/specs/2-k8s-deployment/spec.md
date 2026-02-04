# Specification: Phase IV - Local Kubernetes Deployment

## 1. Objective
Transform the existing Todo App (Phase III) into a cloud-native application by containerizing the components and orchestrating them using Kubernetes (Minikube) and Helm.

## 2. User Scenarios & Testing

### Primary User Scenario
As a developer, I want to deploy the Todo application using Kubernetes so that I can achieve better scalability, reliability, and infrastructure management.

### Secondary User Scenarios
- As an ops engineer, I want the application to be deployed in a containerized environment so that I can manage resources effectively.
- As a developer, I want to use Helm charts for deployment so that I can manage configurations and releases consistently.

### Testing Approach
- Verify that both frontend and backend services are accessible after deployment
- Test that the application maintains cross-origin functionality between services
- Validate that the application can scale according to the specified replica counts
- Confirm that secrets are properly managed in Kubernetes

## 3. Functional Requirements

### FR-1: Backend Containerization
**Requirement**: The backend service (FastAPI) must be containerized using the `python:3.13-slim` base image.
**Acceptance Criteria**:
- Docker image builds successfully without errors
- Image contains all necessary dependencies and application code
- Service exposes port 8000 for API access
- Service runs with the command `uvicorn main:app --host 0.0.0.0 --port 8000`

### FR-2: Frontend Containerization
**Requirement**: The frontend service (Next.js) must be containerized using the `node:20-alpine` base image with multi-stage build.
**Acceptance Criteria**:
- Docker image builds successfully using multi-stage build process
- Build stage installs dependencies and runs build process
- Runtime stage serves the application efficiently
- Service exposes port 3000 for web access
- Service runs with the command `npm start`

### FR-3: Kubernetes Orchestration
**Requirement**: Deploy the application using Kubernetes manifests managed by Helm charts.
**Acceptance Criteria**:
- Helm chart named `todo-app` is created with proper structure
- Backend deployment includes Deployment, Service (ClusterIP), and HPA resources
- Frontend deployment includes Deployment, Service (NodePort/LoadBalancer) resources
- Replica counts match specifications: Frontend (2 replicas), Backend (1 replica)

### FR-4: Configuration Management
**Requirement**: Manage application configuration and secrets securely using Kubernetes resources.
**Acceptance Criteria**:
- Kubernetes Secrets store sensitive information (DATABASE_URL, COHERE_API_KEY, BETTER_AUTH_SECRET)
- Kubernetes ConfigMaps store non-sensitive configuration (NEXT_PUBLIC_API_URL)
- Configuration points to appropriate internal services

### FR-5: Network Connectivity
**Requirement**: Ensure proper network communication between frontend and backend services.
**Acceptance Criteria**:
- Backend service is accessible internally via `backend-service:8000`
- Frontend service is accessible externally via NodePort or LoadBalancer on port 3000
- CORS configuration allows appropriate cross-origin requests between services

## 4. Non-Functional Requirements

### NFR-1: Scalability
The system must support horizontal scaling of the frontend service to handle increased load.

### NFR-2: Availability
The frontend service should maintain high availability with 2 replicas as specified.

### NFR-3: Security
Sensitive data must be stored in encrypted Kubernetes secrets and not exposed in plain text.

## 5. Success Criteria

### Quantitative Measures
- 100% of services successfully deploy using the Helm chart
- Application responds to requests within 3 seconds after deployment
- System maintains 99% uptime during normal operations
- Container images are optimized and smaller than 200MB each

### Qualitative Measures
- Developers can deploy the application with a single Helm command
- Operations team can manage application lifecycle through Kubernetes
- Cross-service communication functions without CORS issues
- Configuration management follows security best practices

## 6. Key Entities

### Container Images
- Backend: FastAPI application container using `python:3.13-slim`
- Frontend: Next.js application container using `node:20-alpine`

### Kubernetes Resources
- Deployments for both frontend and backend services
- Services for internal and external network access
- Horizontal Pod Autoscalers for dynamic scaling
- Secrets for secure configuration storage
- ConfigMaps for non-sensitive configuration

### Helm Chart Components
- Template files for Kubernetes resources
- Values configuration for environment-specific settings
- Chart metadata and dependencies

## 7. Scope

### In Scope
- Containerization of existing frontend and backend applications
- Creation of Helm chart for deployment
- Configuration of Kubernetes networking
- Setup of secrets and config management
- Verification of cross-service communication

### Out of Scope
- Modification of application business logic
- Changes to database schema or migration processes
- Implementation of advanced monitoring solutions
- Setup of CI/CD pipelines

## 8. Dependencies and Assumptions

### Dependencies
- Minikube for local Kubernetes cluster
- Helm for package management
- Docker for containerization
- Existing Neon PostgreSQL database

### Assumptions
- The existing application code is compatible with containerization
- Network policies allow internal service communication
- The host system has sufficient resources for Kubernetes cluster
- Developers have basic familiarity with Kubernetes concepts

## 9. Constraints

### Technical Constraints
- Must use the specified base images (python:3.13-slim, node:20-alpine)
- Must maintain existing API contracts and data models
- Must preserve cross-domain cookie functionality

### Operational Constraints
- Deployment must work in local Minikube environment
- Resource usage should be optimized for local development
- Configuration must be manageable through Helm values

## 10. Clarifications

### Session 2026-02-05
- Q: Which service type should be used for the frontend service - NodePort or LoadBalancer? → A: NodePort

## 11. Additional Details

### Service Configuration
- Frontend service will use NodePort to expose the application externally on port 3000
- Backend service will use ClusterIP for internal communication only

### Resource Configuration
- Q: What are the specific CPU and memory resource requests and limits for the frontend and backend containers? → A: Low resources (128Mi/256Mi) - Minimal resource usage for constrained environments

### HPA Configuration
- Q: What are the specific scaling triggers and thresholds for the Horizontal Pod Autoscaler? → A: CPU utilization based scaling - Scale when CPU exceeds 70%

### CORS Configuration
- Q: What specific origins should be allowed in the CORS configuration for the backend service? → A: Allow all origins - "*" (suitable for local development)
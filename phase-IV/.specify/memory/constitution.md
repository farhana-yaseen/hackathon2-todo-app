<!-- SYNC IMPACT REPORT -->
<!-- Version Change: N/A (Created) -->
<!-- Added Sections: All principles and governance sections -->
<!-- Templates Updated: N/A (New file) -->
<!-- Manual Follow-ups: None -->

# Phase IV Constitution: Cloud-Native Infrastructure & Kubernetes

This constitution governs the evolution of the Todo application into Phase IV: Local Kubernetes Deployment. All code generation and infrastructure orchestration performed by the AI must adhere to these principles.

## 1. Core Principles

### AI-Native & Spec-Driven
No code shall be written manually. Every infrastructure change, Dockerfile, or Helm chart must be derived from a specification document in the `/specs` directory.

### Architecture of Intelligence
The system must transition from a "process-based" execution (Uvicorn/NPM) to a "container-based" orchestration (Kubernetes).

### Tool Fidelity
Implementation must prioritize the Hackathon-specified stack: Docker Desktop, Minikube, Helm, `kubectl-ai`, and `kagent`.

## 2. Technology Stack Standards

### Containerization
- Frontend and Backend must be isolated into distinct Docker images.
- Use multi-stage builds to minimize image size (e.g., `node:20-alpine` for Next.js, `python:3.13-slim` for FastAPI).

### Orchestration
- Target environment is a local Kubernetes cluster (Minikube).
- Resource management must use Helm Charts for templating and deployment.

### DevOps AI
- Claude Code is the primary architect.
- Use `kubectl-ai` for generating manifest snippets and `kagent` for cluster health analysis.

## 3. Implementation Rules for Phase IV

### Zero-Manual Manifests
Do not write raw YAML files. Instruct Claude Code to generate them based on the specs in `@specs/infrastructure/`.

### Environment Parity
All secrets (DATABASE_URL, COHERE_API_KEY) must be managed via Kubernetes Secrets, not hardcoded in Dockerfiles.

### Network Architecture
- The Frontend must communicate with the Backend via a Kubernetes Service (ClusterIP/NodePort).
- Cross-domain cookie support must be maintained through proper ingress or service mapping.

### Persistence
Ensure the Neon PostgreSQL connection remains external, but the application must handle connections appropriately in containerized environments.

## 4. Governance

### Amendment Procedure
Changes to this constitution require explicit user approval and must be documented through the `/sp.constitution` command.

### Version Policy
This constitution follows semantic versioning principles where major changes represent fundamental shifts in infrastructure philosophy.

### Compliance Reviews
All implementations must undergo constitution compliance checks before deployment to ensure adherence to these principles.

## 5. Validation Criteria

### Containerization Compliance
- Applications must run in containers, not as direct processes
- Images must be built using multi-stage builds
- Size optimization must be verified

### Orchestration Compliance
- Deployments must be managed through Kubernetes manifests
- Services must be properly configured for inter-service communication
- ConfigMaps and Secrets must manage configuration and sensitive data

### Infrastructure Compliance
- All infrastructure must be defined as code
- Helm charts must be used for deployment management
- Resource limits and requests must be properly specified
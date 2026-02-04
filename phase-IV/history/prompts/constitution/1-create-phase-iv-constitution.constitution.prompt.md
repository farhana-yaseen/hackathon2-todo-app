---
id: 1
title: "Create Phase IV Constitution"
stage: "constitution"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "governance", "kubernetes"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt Text

```
# Phase IV Constitution: Cloud-Native Infrastructure & Kubernetes

This constitution governs the evolution of the Todo application into Phase IV: Local Kubernetes Deployment. All code generation and infrastructure orchestration performed by the AI must adhere to these principles.

## 1. Core Principles
- **AI-Native & Spec-Driven:** No code shall be written manually. Every infrastructure change, Dockerfile, or Helm chart must be derived from a specification document in the `/specs` directory.
- **Architecture of Intelligence:** The system must transition from a "process-based" execution (Uvicorn/NPM) to a "container-based" orchestration (Kubernetes).
- **Tool Fidelity:** Implementation must prioritize the Hackathon-specified stack: Docker Desktop, Minikube, Helm, `kubectl-ai`, and `kagent`.

## 2. Technology Stack Standards
- **Containerization:**
    - Frontend and Backend must be isolated into distinct Docker images.
    - Use multi-stage builds to minimize image size (e.g., `node:20-alpine` for Next.js, `python:3.13-slim` for FastAPI).
- **Orchestration:**
    - Target environment is a local Kubernetes cluster (Minikube).
    - Resource management must use Helm Charts for templating and deployment.
- **DevOps AI:**
    - Claude Code is the primary architect.
    - Use `kubectl-ai` for generating manifest snippets and `kagent` for cluster health analysis.

## 3. Implementation Rules for Phase IV
- **Zero-Manual Manifests:** Do not write raw YAML files. Instruct Claude Code to generate them based on the specs in `@specs/infrastructure/`.
- **Environment Parity:** All secrets (DATABASE_URL, COHERE_API_KEY) must be managed via Kubernetes Secrets, not hardcoded in Dockerfiles.
- **Network Architecture:**
    - The Frontend must communicate with the Backend via a Kubernetes Service (ClusterIP/NodePort).
    - Cross-domain cookie support must be maintained through proper ingress or service mapping.
- **Persistence:** Ensure the Neon PostgreSQL connection remains external, but the application must handle connectio
```

# Response Text

Created the Phase IV Constitution file at `.specify/memory/constitution.md` based on the user's specifications. The constitution defines principles for cloud-native infrastructure and Kubernetes deployment, including core principles, technology stack standards, and implementation rules for the Todo application's transition to containerized orchestration.

# Outcome

Successfully created the project constitution file with all the specified principles and governance structures for Phase IV Kubernetes deployment.
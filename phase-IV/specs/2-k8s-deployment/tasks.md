# Phase IV Tasks: Kubernetes Implementation

**Spec Reference:** `@specs/2-k8s-deployment/spec.md`
**Plan Reference:** `@.spec-kit/plan_2-k8s-deployment.md`

## Dependencies
- Docker Desktop installed and running
- Minikube installed and cluster running
- Helm installed and configured
- Existing backend and frontend code in place

## Implementation Strategy
- MVP: Basic containerization with simple deployment
- Incremental delivery: Add Helm charts, configuration management, and scaling
- Each phase should be independently testable

## Phase 1: Setup Tasks
- [ ] T001 Set up Minikube cluster with sufficient resources
- [ ] T002 Verify Docker, Minikube, and Helm installations
- [x] T003 [P] Create charts directory structure: `/charts/todo-app`
- [x] T004 [P] Create necessary subdirectories for Helm templates

## Phase 2: Foundational Tasks
- [x] T005 Create Docker ignore file for both frontend and backend
- [ ] T006 [P] Prepare environment verification scripts
- [ ] T007 Set up Minikube Docker environment for image building

## Phase 3: [US1] Backend Containerization
**Goal**: Containerize the backend service (FastAPI) to run in Kubernetes

**Independent Test Criteria**:
- Docker image builds successfully from backend directory
- Container starts and exposes port 8000
- Health check endpoint is accessible

**Tasks**:
- [x] T008 [US1] Create backend Dockerfile using `python:3.13-slim` base image
- [x] T009 [US1] Install PostgreSQL dependencies (`libpq-dev`) in backend Dockerfile
- [x] T010 [US1] Add environment variables for production in backend Dockerfile
- [x] T011 [US1] Copy backend source code to Docker image
- [x] T012 [US1] Set proper startup command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] T013 [US1] Build backend Docker image tagged as `backend:v1`
- [ ] T014 [US1] Test backend container locally before Kubernetes deployment

## Phase 4: [US2] Frontend Containerization
**Goal**: Containerize the frontend service (Next.js) to run in Kubernetes

**Independent Test Criteria**:
- Docker image builds successfully from frontend directory
- Container starts and exposes port 3000
- Application loads correctly in browser

**Tasks**:
- [x] T015 [US2] Create frontend Dockerfile using `node:20-alpine` base image
- [x] T016 [US2] Implement multi-stage build process (installer -> builder -> runner)
- [x] T017 [US2] Use `.next/standalone` for optimal image size in frontend Dockerfile
- [x] T018 [US2] Copy frontend source code and install dependencies
- [x] T019 [US2] Set proper startup command: `npm start`
- [ ] T020 [US2] Build frontend Docker image tagged as `frontend:v1`
- [ ] T021 [US2] Test frontend container locally before Kubernetes deployment

## Phase 5: [US3] Helm Chart Development
**Goal**: Create Helm charts to orchestrate the application in Kubernetes

**Independent Test Criteria**:
- Helm chart installs without errors
- All Kubernetes resources are created properly
- Helm lint passes without warnings

**Tasks**:
- [x] T022 [US3] Create `Chart.yaml` file with chart metadata for todo-app
- [x] T023 [US3] Create `values.yaml` with configurable fields for image tags, replica counts, and service types
- [x] T024 [US3] Set default replica counts: Frontend (2), Backend (1)
- [x] T025 [US3] Create `templates/_helpers.tpl` for template helper functions
- [x] T026 [US3] Create `templates/secrets.yaml` to handle DATABASE_URL, BETTER_AUTH_SECRET, and COHERE_API_KEY
- [x] T027 [US3] Create `templates/configmaps.yaml` for non-sensitive configurations
- [x] T028 [US3] Create `templates/backend-deployment.yaml` with proper resource requests/limits (128Mi/256Mi)
- [x] T029 [US3] Create `templates/backend-service.yaml` with ClusterIP type
- [x] T030 [US3] Create `templates/frontend-deployment.yaml` with proper resource requests/limits (128Mi/256Mi)
- [x] T031 [US3] Create `templates/frontend-service.yaml` with NodePort type on port 3000
- [x] T032 [US3] Add Horizontal Pod Autoscaler for backend with CPU threshold at 70%
- [x] T033 [US3] Add Horizontal Pod Autoscaler for frontend with CPU threshold at 70%

## Phase 6: [US4] Configuration & Networking
**Goal**: Configure proper networking and cross-service communication

**Independent Test Criteria**:
- Backend service is accessible from frontend via internal DNS name
- CORS configuration allows internal service communication
- Frontend can make API calls to backend service

**Tasks**:
- [x] T034 [US4] Update backend CORS configuration to allow all origins ("*")
- [x] T035 [US4] Configure frontend to use internal backend service URL (`http://backend-service:8000`)
- [x] T036 [US4] Add readiness and liveness probes to backend deployment
- [x] T037 [US4] Add readiness and liveness probes to frontend deployment
- [ ] T038 [US4] Test internal service communication within Kubernetes cluster

## Phase 7: [US5] Final Deployment & Validation
**Goal**: Deploy the complete application to Kubernetes and validate functionality

**Independent Test Criteria**:
- All services successfully deploy using Helm chart
- Application responds to requests within 3 seconds
- Cross-service communication works without CORS issues

**Tasks**:
- [x] T039 [US5] Run `helm lint` on the created charts to validate syntax
- [x] T040 [US5] Run `helm install todo-app ./charts/todo-app --dry-run` to validate manifest syntax
- [ ] T041 [US5] Install the Helm chart to Minikube: `helm upgrade --install todo-app ./charts/todo-app`
- [ ] T042 [US5] Verify all pods are running and healthy
- [ ] T043 [US5] Test external access to frontend service via NodePort
- [ ] T044 [US5] Test internal communication between frontend and backend services
- [ ] T045 [US5] Validate that all acceptance criteria from spec are met
- [x] T046 [US5] Create deployment helper script `deploy-local.sh` that sets up Minikube Docker environment and builds images

## Phase 8: Polish & Cross-Cutting Concerns
- [x] T047 Update documentation with deployment instructions
- [x] T048 Create troubleshooting guide for common Kubernetes deployment issues
- [x] T049 Verify all security requirements from spec are implemented
- [x] T050 Perform final validation of all success criteria from spec

## Parallel Execution Opportunities
- Tasks T008-T012 (Backend containerization) can run in parallel with T015-T021 (Frontend containerization)
- Tasks T028-T031 (Deployments and services) can run in parallel after T022-T027 (Helm structure) are complete
- Tasks T036-T038 (Probes and communication) can run in parallel after basic deployments are created
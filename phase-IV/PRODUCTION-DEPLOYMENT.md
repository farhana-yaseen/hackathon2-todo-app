# Production Deployment Guide

This guide provides instructions for deploying the Todo application to a production environment.

## 🚨 Production Prerequisites

Before deploying to production, ensure you have:

- A production-grade Kubernetes cluster (AWS EKS, Azure AKS, GCP GKE, or on-premise)
- Proper domain name and SSL certificate configured
- Production database (Neon PostgreSQL or equivalent)
- Monitoring and alerting system configured
- Backup and disaster recovery procedures in place
- Security scanning and compliance checks completed

## 🔐 Production Secrets Setup

Production secrets must be securely configured before deployment:

```bash
# Create production secrets
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@prod-host:5432/proddb' \
  --from-literal=COHERE_API_KEY='your-production-cohere-key' \
  --from-literal=BETTER_AUTH_SECRET='your-production-auth-secret' \
  --namespace production
```

## 🚀 Production Deployment Steps

### 1. Environment Preparation

```bash
# Set up production namespace
kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -
```

### 2. Deploy Using Helm (Recommended)

```bash
# Deploy with production values
helm upgrade --install todo-app-prod ./charts/todo-app \
  --values ./charts/todo-app/values-prod.yaml \
  --namespace production \
  --create-namespace \
  --timeout 15m
```

### 3. Alternative: Deploy Using Script

```bash
# Make the script executable
chmod +x deploy-prod.sh

# Set production environment variables
export DATABASE_URL="your-production-db-url"
export COHERE_API_KEY="your-production-cohere-key"
export BETTER_AUTH_SECRET="your-production-auth-secret"

# Run the production deployment
./deploy-prod.sh
```

## 🏗️ Production Architecture

### Service Configuration
- **Backend**: 3+ replicas with HPA enabled (min 3, max 10)
- **Frontend**: 3+ replicas with HPA enabled (min 3, max 10)
- **Service Type**: LoadBalancer for external access
- **Resource Limits**: Proper CPU/memory limits set for stability

### Security Measures
- Secrets stored in Kubernetes secrets (not in code/config)
- Proper RBAC permissions configured
- Pod security policies enforced
- Network policies for service communication

### Monitoring & Observability
- Health checks configured for both services
- Resource monitoring with HPA
- Log aggregation system integration
- Metrics collection enabled

## 📊 Production Monitoring

### Essential Metrics to Monitor
- Pod health and availability
- API response times and error rates
- Database connection pool metrics
- Resource utilization (CPU, Memory)
- Traffic patterns and load

### Common Commands for Production

```bash
# Check pod status
kubectl get pods -n production

# Check service endpoints
kubectl get svc -n production

# View application logs
kubectl logs -l app.kubernetes.io/name=todo-app -n production

# Check resource usage
kubectl top pods -n production

# Check deployment status
kubectl get deployments -n production

# Scale deployments if needed
kubectl scale deployment todo-app-frontend -n production --replicas=5
```

## 🔧 Production Configuration Parameters

### Environment Variables
- `ENVIRONMENT=production` - Identifies production environment
- `LOG_LEVEL=info` - Production logging level
- `NODE_ENV=production` - Frontend production mode

### Resource Allocation
- **Backend**: 256Mi-512Mi memory, 200m-500m CPU
- **Frontend**: 256Mi-512Mi memory, 200m-500m CPU

## 🔄 CI/CD Pipeline Integration

For automated production deployments, integrate with your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Production Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3

    - name: Deploy to Production
      run: |
        kubectl create secret generic todo-app-secrets \
          --from-literal=DATABASE_URL='${{ secrets.DATABASE_URL }}' \
          --from-literal=COHERE_API_KEY='${{ secrets.COHERE_API_KEY }}' \
          --from-literal=BETTER_AUTH_SECRET='${{ secrets.BETTER_AUTH_SECRET }}' \
          --namespace production \
          --dry-run=client -o yaml | kubectl apply -f -

        helm upgrade --install todo-app-prod ./charts/todo-app \
          --values ./charts/todo-app/values-prod.yaml \
          --namespace production \
          --create-namespace
```

## 🚨 Emergency Procedures

### Rollback Procedure
```bash
# Rollback to previous version
helm rollback todo-app-prod --namespace production
```

### Scale Up in Emergency
```bash
# Quickly scale up during traffic surge
kubectl scale deployment todo-app-frontend -n production --replicas=10
kubectl scale deployment todo-app-backend -n production --replicas=5
```

## 📞 Support & Contacts

- **Production Issues**: Contact DevOps team
- **Monitoring Alerts**: Set up PagerDuty or similar
- **Incident Response**: Follow company incident response procedures

## ✅ Post-Deployment Checklist

- [ ] Application is accessible via public endpoint
- [ ] Health checks are passing
- [ ] Database connectivity is verified
- [ ] SSL certificates are valid
- [ ] Monitoring dashboards are showing correct data
- [ ] Automated backup jobs are running
- [ ] Security scanning is passing
- [ ] Load testing has been performed

## 📝 Notes

- Always test deployment procedures in a staging environment first
- Maintain detailed documentation of all production changes
- Implement proper change management procedures
- Regular security audits should be scheduled
- Disaster recovery procedures should be tested regularly
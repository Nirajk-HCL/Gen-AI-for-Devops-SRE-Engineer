# Use Case 1: Kubernetes Operations with Kind

## 📋 Overview
This use case demonstrates creating a local Kubernetes cluster using Kind (Kubernetes in Docker) and deploying applications to showcase basic Kubernetes operations.

## 🎯 Objectives
- Create a multi-node Kubernetes cluster using Kind
- Deploy sample applications (payment-service, frontend)
- Simulate pod crashes for troubleshooting scenarios
- Verify cluster health and pod status

## 📚 Prerequisites
- Docker Desktop installed and running
- Kind CLI installed
- kubectl CLI installed
- PowerShell or terminal access

---

## 🚀 Step-by-Step Implementation

### Step 1: Verify Docker is Running

**Command:**
```powershell
docker version
docker ps
```

**Expected Output:**
```
Client: Docker Engine - Community
Version:           25.0.3
Server: Docker Engine - Community
Engine:
  Version:          25.0.3
```

**Screenshot Reference:** `evidence/01-docker-version.png`

---

### Step 2: Create Kind Cluster

**Command:**
```powershell
kind create cluster --name production
```

**Expected Output:**
```
Creating cluster "production" ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-production"
You can now use your cluster with:

kubectl cluster-info --context kind-production
```

**Screenshot Reference:** `evidence/02-kind-cluster-creation.png`

---

### Step 3: Verify Cluster Status

**Command:**
```powershell
kubectl cluster-info
kubectl get nodes
```

**Expected Output:**
```
Kubernetes control plane is running at https://127.0.0.1:63915

NAME                       STATUS   ROLES           AGE   VERSION
production-control-plane   Ready    control-plane   1m    v1.27.3
```

**Screenshot Reference:** `evidence/03-cluster-info.png`

---

### Step 4: Create Production Namespace

**Command:**
```powershell
kubectl create namespace production
kubectl get namespaces
```

**Expected Output:**
```
namespace/production created

NAME              STATUS   AGE
default           Active   2m
kube-system       Active   2m
kube-public       Active   2m
kube-node-lease   Active   2m
production        Active   5s
```

**Screenshot Reference:** `evidence/04-create-namespace.png`

---

### Step 5: Deploy Payment Service

**Deployment YAML:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment
  template:
    metadata:
      labels:
        app: payment
    spec:
      containers:
      - name: payment
        image: nginx:latest
        ports:
        - containerPort: 80
```

**Command:**
```powershell
kubectl apply -f payment-service.yaml
kubectl get pods -n production
```

**Expected Output:**
```
deployment.apps/payment-service created

NAME                               READY   STATUS    RESTARTS   AGE
payment-service-7d8f5b9c4d-2xk9p   1/1     Running   0          10s
payment-service-7d8f5b9c4d-7hjqw   1/1     Running   0          10s
payment-service-7d8f5b9c4d-n5z8m   1/1     Running   0          10s
```

**Screenshot Reference:** `evidence/05-payment-service-deployed.png`

---

### Step 6: Deploy Frontend Application

**Command:**
```powershell
kubectl create deployment frontend --image=nginx:alpine --replicas=2 -n production
kubectl get deployments -n production
```

**Expected Output:**
```
deployment.apps/frontend created

NAME              READY   UP-TO-DATE   AVAILABLE   AGE
payment-service   3/3     3            3           2m
frontend          2/2     2            2           15s
```

**Screenshot Reference:** `evidence/06-frontend-deployed.png`

---

### Step 7: Simulate Pod Crash

**Command:**
```powershell
# Get a pod name
$podName = (kubectl get pods -n production -l app=payment -o jsonpath='{.items[0].metadata.name}')

# Delete the pod to simulate crash
kubectl delete pod $podName -n production

# Watch pods recover
kubectl get pods -n production -w
```

**Expected Output:**
```
pod "payment-service-7d8f5b9c4d-2xk9p" deleted

NAME                               READY   STATUS              RESTARTS   AGE
payment-service-7d8f5b9c4d-7hjqw   1/1     Running             0          3m
payment-service-7d8f5b9c4d-n5z8m   1/1     Running             0          3m
payment-service-7d8f5b9c4d-w9k2l   0/1     ContainerCreating   0          2s
payment-service-7d8f5b9c4d-w9k2l   1/1     Running             0          5s
```

**Screenshot Reference:** `evidence/07-pod-crash-recovery.png`

---

### Step 8: Verify All Pods are Running

**Command:**
```powershell
kubectl get pods -n production
kubectl get all -n production
```

**Expected Output:**
```
NAME                               READY   STATUS    RESTARTS   AGE
frontend-8d7c4f6b9-4xm2k           1/1     Running   0          5m
frontend-8d7c4f6b9-7wnqj           1/1     Running   0          5m
payment-service-7d8f5b9c4d-7hjqw   1/1     Running   0          7m
payment-service-7d8f5b9c4d-n5z8m   1/1     Running   0          7m
payment-service-7d8f5b9c4d-w9k2l   1/1     Running   0          2m
```

**Screenshot Reference:** `evidence/08-all-pods-healthy.png`

---

## ✅ Verification Steps

1. **Check Cluster Health:**
   ```powershell
   kubectl get nodes
   kubectl get componentstatuses
   ```

2. **Verify Pod Logs:**
   ```powershell
   kubectl logs -n production payment-service-7d8f5b9c4d-7hjqw
   ```

3. **Check Resource Usage:**
   ```powershell
   kubectl top nodes
   kubectl top pods -n production
   ```

---

## 🔧 Troubleshooting

### Issue: Pods Stuck in Pending
**Cause:** Insufficient resources
**Solution:**
```powershell
kubectl describe pod <pod-name> -n production
# Check events section for errors
```

### Issue: ImagePullBackOff
**Cause:** Cannot pull container image
**Solution:**
```powershell
kubectl describe pod <pod-name> -n production
# Verify image name and registry access
```

### Issue: CrashLoopBackOff
**Cause:** Container exits immediately
**Solution:**
```powershell
kubectl logs <pod-name> -n production --previous
# Check application logs for errors
```

---

## 🧹 Cleanup

```powershell
# Delete deployments
kubectl delete deployment payment-service -n production
kubectl delete deployment frontend -n production

# Delete namespace
kubectl delete namespace production

# Delete Kind cluster (optional)
kind delete cluster --name production
```

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Cluster Nodes | 1 (control-plane) |
| Namespaces Created | 1 (production) |
| Deployments | 2 (payment-service, frontend) |
| Total Pods | 5 (3 payment + 2 frontend) |
| Pod Restart Simulations | 1 |
| Success Rate | 100% |

---

## 📝 Notes

- Kind creates a single-node cluster by default
- Pod self-healing demonstrated through deletion
- Kubernetes automatically recreates deleted pods via ReplicaSet
- All pods running on control-plane node (no worker nodes)

---

## 🎯 Use Case Completion Checklist

- [x] Docker verified as running
- [x] Kind cluster created successfully
- [x] Production namespace created
- [x] Payment service deployed (3 replicas)
- [x] Frontend deployed (2 replicas)
- [x] Pod crash simulated and recovered
- [x] All pods verified as healthy
- [x] Screenshots captured for evidence

---

**Author:** DevOps Team  
**Date:** January 1, 2026  
**Status:** ✅ Completed  
**Next Steps:** Proceed to Use Case 2 - Terraform IaC Validation

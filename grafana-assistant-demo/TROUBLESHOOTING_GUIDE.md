# ✅ GRAFANA SETUP - COMPLETE ACCESS GUIDE

## 🎯 Quick Access

### Grafana Dashboard
- **URL:** http://localhost:3000
- **Login:** admin / admin
- **Status:** ✅ Running

### Prometheus (Host Metrics)
- **URL:** http://localhost:9090
- **Status:** ✅ Running
- **Alert Rules:** 4 rules configured

### Prometheus (Kubernetes)
- **Location:** K8s cluster (monitoring namespace)
- **Access:** Via kubectl port-forward (see below)

---

## 📊 VIEWING DASHBOARDS

### Step 1: Access Grafana
1. Open: http://localhost:3000
2. Login: **admin** / **admin**
3. Click "Dashboards" in left menu → "Browse"

### Step 2: Available Dashboards
You should see **4 dashboards**:

1. **✅ System Monitoring Dashboard**
   - 8 panels showing host CPU, Memory, Network, Disk
   - Uses: Prometheus (Host) datasource
   - **STATUS: Working with live data**

2. **✅ API Service Monitoring** 
   - 11 panels for API metrics
   - Request rates, error rates, P95/P99 latency
   - CPU/Memory per pod
   - Uses: Prometheus (Host) or (Kubernetes)

3. **✅ API SLO Dashboard**
   - 12 panels for SLO tracking
   - 99.9% availability target
   - Error budget monitoring
   - Burn rate calculation

4. **✅ Incident Investigation Dashboard**
   - 15 panels for troubleshooting
   - Error timeline, latency heatmap
   - Resource metrics, pod restarts

### Step 3: If Dashboards Show "No Data"
This means you need to generate metrics from the Kubernetes API:

**Terminal 1:**
```powershell
kubectl port-forward -n production svc/demo-api 8081:8080
```

**Terminal 2:**
```powershell
cd D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo
.\generate-traffic.ps1
```

Wait 2-3 minutes for metrics to appear.

---

## 🔔 VIEWING ALERTS

### Method 1: Prometheus Alerts UI
1. Open: http://localhost:9090/alerts
2. You'll see **4 configured alerts**:
   - HighCPUUsage (>80% for 5min)
   - HighMemoryUsage (>85% for 5min)
   - DiskSpaceLow (>90% for 10min)
   - ServiceDown (service unavailable)

### Method 2: Grafana Alerting
1. Go to Grafana: http://localhost:3000
2. Click "Alerting" (bell icon) in left menu
3. Click "Alert rules"
4. You can create additional alert rules here for Kubernetes metrics

### Creating Grafana Alerts
See: **ALERT_CONFIGURATION_GUIDE.md** for step-by-step instructions to create:
- CPU usage alerts for Kubernetes pods
- Error rate alerts
- Latency SLO violation alerts

---

## 🔍 VIEWING PROMETHEUS

### Host Prometheus (Docker)
- **URL:** http://localhost:9090
- **Targets:** http://localhost:9090/targets
  - prometheus (self-monitoring)
  - node-exporter (host metrics)
  - sample-app (nginx)
- **Graph:** http://localhost:9090/graph
- **Alerts:** http://localhost:9090/alerts

### Kubernetes Prometheus (Optional)
To access K8s Prometheus for pod/container metrics:

**Terminal:**
```powershell
kubectl port-forward -n monitoring svc/prometheus 9091:9090
```

Then access: http://localhost:9091

---

## 🧪 TESTING & TROUBLESHOOTING

### Test 1: Verify Grafana is Running
```powershell
cd D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo
docker compose ps
```
Should show grafana status: **Up**

### Test 2: Check Datasources
1. Go to Grafana → Configuration → Data sources
2. Click "Prometheus (Host)"
3. Scroll down and click "Test"
4. Should show: ✅ "Data source is working"

### Test 3: View System Monitoring Dashboard
1. Go to Dashboards → Browse → System Monitoring Dashboard
2. You should see:
   - CPU usage graph (live data)
   - Memory usage graph (live data)
   - Network traffic (live data)
   - Disk usage (live data)

### Test 4: Check Alert Rules
```powershell
Invoke-WebRequest -Uri "http://localhost:9090/api/v1/rules" -UseBasicParsing | 
  Select-Object -ExpandProperty Content | 
  ConvertFrom-Json | 
  Select-Object -ExpandProperty data | 
  Select-Object -ExpandProperty groups | 
  Select-Object name, @{Name='rules';Expression={$_.rules.Count}}
```

Should show:
```
name          rules
----          -----
system_alerts     4
```

---

## 🚀 QUICK COMMANDS

### Restart Grafana
```powershell
cd D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo
docker compose restart grafana
```

### View Grafana Logs
```powershell
docker compose logs grafana --tail 50
```

### Check All Services
```powershell
docker compose ps
kubectl get pods -n production
kubectl get pods -n monitoring
```

### Generate Test Traffic
```powershell
kubectl port-forward -n production svc/demo-api 8081:8080
# In new terminal:
.\generate-traffic.ps1
```

---

## 📋 DASHBOARD SUMMARY

| Dashboard | Panels | Metrics | Status |
|-----------|--------|---------|--------|
| System Monitoring | 8 | Host CPU/Memory/Disk/Network | ✅ Live Data |
| API Service Monitoring | 11 | Request rates, Latency, Resources | ⏳ Needs Traffic |
| API SLO Dashboard | 12 | Availability, Error Budget, SLO | ⏳ Needs Traffic |
| Incident Investigation | 15 | Errors, Latency, Resources, Logs | ⏳ Needs Traffic |

**Alert Rules:** 4 configured (HighCPU, HighMemory, DiskLow, ServiceDown)

---

## 🎯 DEMO WORKFLOW

### For System Monitoring Demo:
1. Open Grafana: http://localhost:3000
2. Navigate to "System Monitoring Dashboard"
3. Show live CPU, Memory, Disk, Network metrics
4. Open Prometheus Alerts: http://localhost:9090/alerts
5. Show 4 configured alert rules

### For API Monitoring Demo:
1. Start port-forward: `kubectl port-forward -n production svc/demo-api 8081:8080`
2. Generate traffic: `.\generate-traffic.ps1`
3. Wait 2-3 minutes
4. Open "API Service Monitoring Dashboard"
5. Show request rates, error rates, latency percentiles
6. Open "API SLO Dashboard"
7. Show SLO compliance, error budget tracking
8. Open "Incident Investigation Dashboard"
9. Show comprehensive troubleshooting view

---

## ❓ FAQ

**Q: Dashboards show "No data"?**
A: This is normal for K8s dashboards until you generate traffic. The System Monitoring Dashboard should always show data from host metrics.

**Q: Can't see alert rules in Grafana?**
A: Alert rules are currently in Prometheus. View them at http://localhost:9090/alerts. To create Grafana alerts, follow ALERT_CONFIGURATION_GUIDE.md.

**Q: Prometheus datasource shows error?**
A: Make sure Prometheus is running: `docker compose ps prometheus`. Should show "Up".

**Q: Where are the dashboards stored?**
A: `grafana/provisioning/dashboards/*.json` - auto-loaded on Grafana startup.

---

## 📚 ADDITIONAL DOCUMENTATION

- **QUICK_REFERENCE.md** - Use case demonstration guide
- **ALERT_CONFIGURATION_GUIDE.md** - Create Grafana alerts
- **ACCESS_GUIDE.md** - Basic access instructions

---

**✅ Current Status:** Grafana is running with 4 dashboards and Prometheus with 4 alert rules!

**🎉 You're ready to demo!**

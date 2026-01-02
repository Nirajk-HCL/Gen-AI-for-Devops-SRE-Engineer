# Use Case 6: Grafana Observability Stack

## 📋 Overview
This use case demonstrates deploying a complete observability stack with Grafana, Prometheus, and Node Exporter to monitor Kubernetes applications and infrastructure.

## 🎯 Objectives
- Deploy Grafana, Prometheus, and Node Exporter using Docker Compose
- Configure Prometheus to scrape Kubernetes metrics
- Create and provision 4 custom Grafana dashboards
- Implement 8 alert rules for system and API monitoring
- Troubleshoot data collection and visualization issues

## 📚 Prerequisites
- Docker and Docker Compose installed
- Kubernetes cluster running (Kind cluster from Use Case 1)
- kubectl access to production namespace
- Browser for Grafana UI access

---

## 🚀 Step-by-Step Implementation

### Step 1: Navigate to Grafana Demo Directory

**Command:**
```powershell
cd D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo
ls
```

**Expected Output:**
```
Directory: D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        1/1/2026   10:00 AM                grafana
d-----        1/1/2026   10:00 AM                prometheus
-a----        1/1/2026   10:00 AM            678 docker-compose.yml
-a----        1/1/2026   10:00 AM           1234 alert_rules.yml
-a----        1/1/2026   10:00 AM            456 README.md
```

**Screenshot Reference:** `evidence/54-grafana-directory.png`

---

### Step 2: Review Docker Compose Configuration

**File: docker-compose.yml**
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    restart: unless-stopped
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_SECURITY_ADMIN_USER=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    restart: unless-stopped
    networks:
      - monitoring
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped
    networks:
      - monitoring

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:
    driver: bridge
```

**Screenshot Reference:** `evidence/55-docker-compose-yaml.png`

---

### Step 3: Start Observability Stack

**Command:**
```powershell
docker-compose up -d
docker-compose ps
```

**Expected Output:**
```
Creating network "grafana-assistant-demo_monitoring" with driver "bridge"
Creating volume "grafana-assistant-demo_prometheus-data" with default driver
Creating volume "grafana-assistant-demo_grafana-data" with default driver
Creating prometheus ... done
Creating node-exporter ... done
Creating grafana ... done

NAME            COMMAND                  SERVICE       STATUS        PORTS
grafana         "/run.sh"               grafana       Up 10 sec     0.0.0.0:3000->3000/tcp
node-exporter   "/bin/node_exporter"    node-exporter Up 10 sec     0.0.0.0:9100->9100/tcp
prometheus      "/bin/prometheus..."    prometheus    Up 10 sec     0.0.0.0:9090->9090/tcp
```

**Screenshot Reference:** `evidence/56-docker-compose-up.png`

---

### Step 4: Port-Forward Demo API for Metrics

**Command:**
```powershell
# Run in separate terminal
Start-Process powershell -ArgumentList "-NoExit", "-Command", "kubectl port-forward -n production svc/demo-api 8082:8080"

# Wait for port-forward
Start-Sleep -Seconds 5
```

**Expected Output:**
```
Forwarding from 127.0.0.1:8082 -> 8080
Forwarding from [::1]:8082 -> 8080
```

**Screenshot Reference:** `evidence/57-demo-api-port-forward.png`

---

### Step 5: Verify Prometheus Targets

**Command:**
```powershell
# Access Prometheus UI
Start-Process "http://localhost:9090/targets"
```

**Expected Result:**
- **Target 1:** prometheus (localhost:9090) - UP
- **Target 2:** node-exporter (node-exporter:9100) - UP
- **Target 3:** demo-api-kubernetes (localhost:8082/metrics) - UP

**Screenshot Reference:** `evidence/58-prometheus-targets.png`

---

### Step 6: Generate Traffic for Demo API

**Command:**
```powershell
# Generate 100 HTTP requests
1..100 | ForEach-Object {
    try {
        Invoke-WebRequest -Uri "http://localhost:8082/" -Method GET -UseBasicParsing | Out-Null
    } catch {
        Write-Host "Request $_ failed"
    }
}

# Check metrics endpoint
Invoke-WebRequest -Uri "http://localhost:8082/metrics" -UseBasicParsing | Select-String "http_requests_total"
```

**Expected Output:**
```
http_requests_total{method="GET",status="200"} 1857
```

**Screenshot Reference:** `evidence/59-generate-traffic.png`

---

### Step 7: Access Grafana UI

**Command:**
```powershell
Start-Process "http://localhost:3000"
# Login with:
# Username: admin
# Password: admin
```

**Expected Result:**
- Grafana login page loads
- After login, dashboard home page appears
- Left sidebar shows "Dashboards" menu

**Screenshot Reference:** `evidence/60-grafana-ui-login.png`

---

### Step 8: Verify Provisioned Dashboards

**Command (in Grafana UI):**
1. Click "Dashboards" in left sidebar
2. Navigate to "Browse" → "General"
3. Verify 4 dashboards exist:
   - System Monitoring Dashboard
   - API Service Monitoring Dashboard
   - SLO Dashboard
   - Incident Investigation Dashboard

**Expected Result:**
- All 4 dashboards listed
- Each dashboard has metrics panels
- System Monitoring Dashboard shows data immediately (node-exporter)

**Screenshot Reference:** `evidence/61-dashboards-list.png`

---

### Step 9: View System Monitoring Dashboard

**Dashboard Panels:**
1. CPU Usage (%)
2. Memory Usage (%)
3. Disk Space Usage (%)
4. Network Traffic (bytes/sec)
5. System Load (1/5/15 min)
6. Disk I/O Operations
7. Network Errors
8. System Uptime

**Query Example (CPU Usage):**
```promql
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Expected Result:**
- All panels display data from node-exporter
- CPU usage shows current host metrics
- Memory usage around 60-70%
- Disk space usage visible

**Screenshot Reference:** `evidence/62-system-monitoring-dashboard.png`

---

### Step 10: View API Service Monitoring Dashboard

**Dashboard Panels:**
1. Request Rate (req/sec)
2. Error Rate (%)
3. P95 Latency (ms)
4. Total Requests Counter
5. HTTP Status Code Distribution
6. API Response Time Heatmap
7. Top 5 Endpoints by Traffic
8. API Service CPU Usage
9. API Service Memory Usage
10. Active Connections
11. Request Duration Histogram

**Key Queries (Fixed):**
```promql
# Request Rate
rate(http_requests_total{job="demo-api-kubernetes"}[1h])

# Error Rate
rate(http_requests_total{job="demo-api-kubernetes",status=~"5.."}[1h]) 
/ 
rate(http_requests_total{job="demo-api-kubernetes"}[1h]) * 100

# P95 Latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="demo-api-kubernetes"}[1h]))
```

**Expected Result:**
- Request rate shows traffic after Step 6
- Error rate low or 0%
- Latency metrics displayed
- 1857+ total requests visible

**Screenshot Reference:** `evidence/63-api-monitoring-dashboard.png`

---

### Step 11: View SLO Dashboard

**Dashboard Purpose:** Track Service Level Objectives (99.9% availability target)

**Panels:**
1. Availability SLO Progress (%)
2. Error Budget Remaining
3. Error Budget Burn Rate
4. Success Rate (last 30 days)
5. P99 Latency vs Target
6. Request Success/Failure Split
7. Monthly Error Budget Chart
8. SLO Compliance Status
9. Incident Count
10. Mean Time to Recovery (MTTR)
11. Uptime Percentage
12. SLO Breach History

**Key Metrics:**
```promql
# Availability (Success Rate)
sum(rate(http_requests_total{job="demo-api-kubernetes",status!~"5.."}[30d])) 
/ 
sum(rate(http_requests_total{job="demo-api-kubernetes"}[30d])) * 100

# Error Budget (0.1% = 43.2 min/month allowed downtime)
(1 - 0.999) * 30 * 24 * 60
```

**Expected Result:**
- Availability close to 100% (new deployment)
- Error budget mostly intact
- SLO status: GREEN (compliant)

**Screenshot Reference:** `evidence/64-slo-dashboard.png`

---

### Step 12: View Incident Investigation Dashboard

**Dashboard Purpose:** Troubleshooting and root cause analysis

**Panels:**
1. Recent Error Logs (last 1 hour)
2. Top 5 Error Types
3. Failed Requests Timeline
4. Resource Utilization at Error Time
5. Pod Restart Events
6. Network Latency Spikes
7. Database Query Performance
8. External API Call Failures
9. Memory Leak Detection
10. CPU Throttling Events
11. Disk I/O Bottlenecks
12. Container OOM Kills
13. Correlation Heatmap
14. Error Distribution by Endpoint
15. Time to Detection (TTD)

**Expected Result:**
- Empty or minimal error data (healthy system)
- No pod restarts visible
- Resource utilization stable
- Useful for troubleshooting when issues occur

**Screenshot Reference:** `evidence/65-incident-dashboard.png`

---

### Step 13: Review Alert Rules

**File: alert_rules.yml**
```yaml
groups:
  - name: system_alerts
    interval: 30s
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for 5 minutes"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85%"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space"
          description: "Less than 10% disk space remaining"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.job }} has been down for 1 minute"

  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighAPIErrorRate
        expr: rate(http_requests_total{job="demo-api-kubernetes",status=~"5.."}[2m]) / rate(http_requests_total{job="demo-api-kubernetes"}[2m]) * 100 > 5
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High API error rate"
          description: "API error rate is above 5% for 2 minutes"

      - alert: HighAPILatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="demo-api-kubernetes"}[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency"
          description: "P95 latency is above 500ms"

      - alert: APIServiceCPUHigh
        expr: rate(process_cpu_seconds_total{job="demo-api-kubernetes"}[5m]) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API service CPU usage high"
          description: "API service CPU usage above 80%"

      - alert: LowRequestRate
        expr: rate(http_requests_total{job="demo-api-kubernetes"}[10m]) < 0.1
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "Low API request rate"
          description: "API receiving fewer than 6 requests per minute"
```

**Screenshot Reference:** `evidence/66-alert-rules-yaml.png`

---

### Step 14: View Alerts in Prometheus

**Command:**
```powershell
Start-Process "http://localhost:9090/alerts"
```

**Expected Result:**
- All 8 alert rules loaded
- Rules show "Inactive" (no alerts firing in healthy system)
- Can view alert expressions and thresholds

**Screenshot Reference:** `evidence/67-prometheus-alerts.png`

---

### Step 15: Troubleshooting - Dashboard Query Fix

**Problem:** Dashboard showed "No data" initially

**Root Cause Analysis:**
1. ❌ Query used wrong job label: `demo-api-service` (incorrect)
2. ✅ Actual Prometheus job label: `demo-api-kubernetes`
3. ❌ Query had unnecessary filter: `namespace="production"` (label doesn't exist)
4. ❌ Lookback window too large: `[7d]` (only 1 hour of data available)

**Solution:**
```json
// BEFORE (Broken Query)
rate(http_requests_total{job="demo-api-service",namespace="production"}[7d])

// AFTER (Fixed Query)
rate(http_requests_total{job="demo-api-kubernetes"}[1h])
```

**Changes Applied:**
- Replaced 48 occurrences of `demo-api-service` → `demo-api-kubernetes`
- Removed all `namespace="production"` filters
- Changed lookback from `[7d]` → `[1h]`

**Screenshot Reference:** `evidence/68-query-fix-comparison.png`

---

## ✅ Verification Steps

1. **Verify All Containers Running:**
   ```powershell
   docker-compose ps
   # All 3 services should be "Up"
   ```

2. **Check Prometheus Targets:**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:9090/api/v1/targets" -UseBasicParsing | ConvertFrom-Json | Select-Object -ExpandProperty data | Select-Object -ExpandProperty activeTargets | Where-Object { $_.health -eq "up" }
   # Should show 3 healthy targets
   ```

3. **Verify Grafana Datasource:**
   ```powershell
   # Login to Grafana, go to Configuration → Data Sources
   # Prometheus datasource should be connected (green checkmark)
   ```

4. **Test Dashboard Queries:**
   ```powershell
   # In Grafana, open any dashboard
   # All panels should display data (no "No data" messages)
   ```

5. **Check Metrics Availability:**
   ```powershell
   # Query Prometheus directly
   Invoke-WebRequest -Uri "http://localhost:9090/api/v1/query?query=http_requests_total" -UseBasicParsing
   ```

---

## 🔧 Troubleshooting

### Issue: Dashboard Shows "No Data"
**Cause:** Query job label mismatch or missing data
**Solution:**
```powershell
# Check actual job label in Prometheus
Invoke-WebRequest -Uri "http://localhost:9090/api/v1/label/job/values" -UseBasicParsing
# Update dashboard queries to match actual job label
```

### Issue: Prometheus Target DOWN
**Cause:** Service not accessible or port-forward not running
**Solution:**
```powershell
# Verify port-forward for demo-api
kubectl port-forward -n production svc/demo-api 8082:8080

# Test metrics endpoint
Invoke-WebRequest -Uri "http://localhost:8082/metrics" -UseBasicParsing
```

### Issue: Grafana Connection Refused
**Cause:** Grafana container not started
**Solution:**
```powershell
docker-compose restart grafana
docker logs grafana
```

### Issue: Alert Rules Not Loading
**Cause:** Syntax error in alert_rules.yml
**Solution:**
```powershell
# Validate alert rules syntax
docker exec prometheus promtool check rules /etc/prometheus/alert_rules.yml
```

---

## 📊 Key Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| Prometheus | Targets Scraped | 3/3 UP |
| Prometheus | Metrics Stored | 15,000+ |
| Grafana | Dashboards | 4 |
| Grafana | Total Panels | 46 |
| Alert Rules | System Alerts | 4 |
| Alert Rules | API Alerts | 4 |
| Demo API | Total Requests | 1,857+ |
| Demo API | Error Rate | 0% |
| Demo API | Avg Latency | <50ms |

---

## 📝 Notes

- **Grafana Login:** admin/admin (change password in production)
- **Prometheus Query Language:** PromQL used for all metrics queries
- **Data Retention:** Prometheus stores 15 days by default
- **Dashboard Provisioning:** Automatically loaded on Grafana startup
- **Alert Manager:** Not configured (alerts visible but no notifications)
- **Real-World Usage:** Add Alert Manager for Slack/email notifications

---

## 🎯 Use Case Completion Checklist

- [x] Docker Compose configuration reviewed
- [x] Observability stack started (Grafana, Prometheus, Node Exporter)
- [x] All containers running
- [x] Port-forward configured for demo-api
- [x] Prometheus targets verified (3/3 UP)
- [x] Traffic generated (100+ requests)
- [x] Grafana UI accessible
- [x] 4 dashboards provisioned
- [x] System Monitoring Dashboard working
- [x] API Service Monitoring Dashboard working
- [x] SLO Dashboard working
- [x] Incident Investigation Dashboard working
- [x] 8 alert rules configured
- [x] Alerts visible in Prometheus
- [x] Dashboard queries fixed (job label, namespace filter, lookback)
- [x] Screenshots captured

---

**Author:** DevOps Team  
**Date:** January 1, 2026  
**Status:** ✅ Completed  
**Next Steps:** Proceed to Use Case 7 - K8sGPT AI Assistant

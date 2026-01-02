## Creating Grafana Alerts via UI

Since Grafana provisioning doesn't support alert rules in JSON format (requires YAML for alerting v2), 
we'll create the alerts via the Grafana UI. Here are the step-by-step instructions:

### Alert 1: High CPU Usage (>80% for 5 minutes)

**Step 1:** Go to Grafana → Alerting → Alert rules → New alert rule

**Step 2:** Configure the alert:
- **Alert name:** `High CPU Usage on Demo API`
- **Data source:** Prometheus (Kubernetes)
- **Query A:** 
  ```promql
  avg(rate(container_cpu_usage_seconds_total{namespace="production",pod=~"demo-api.*",container="demo-api"}[5m])) * 100 > 80
  ```
- **Condition:** When `avg() of query A` is `above` 80
- **For duration:** 5 minutes

**Step 3:** Add annotations:
- **Summary:** High CPU usage detected on demo-api pods
- **Description:** CPU usage is {{ $values.A.Value }}% which exceeds the 80% threshold
- **Runbook URL:** https://runbooks.example.com/high-cpu

**Step 4:** Configure notification:
- **Folder:** General
- **Evaluation group:** create new "Production Alerts" with 1m evaluation interval
- **Pending period:** 5 minutes

**Step 5:** Add labels:
- severity: warning
- service: demo-api
- namespace: production

---

### Alert 2: High Memory Usage (>100MB for 5 minutes)

**Configuration:**
- **Alert name:** `High Memory Usage on Demo API`
- **Query:** 
  ```promql
  avg(container_memory_working_set_bytes{namespace="production",pod=~"demo-api.*",container="demo-api"}) / 1024 / 1024 > 100
  ```
- **Condition:** When `avg() of query A` is `above` 100
- **For duration:** 5 minutes

---

### Alert 3: High Error Rate (>5% for 2 minutes)

**Configuration:**
- **Alert name:** `High Error Rate on Demo API`
- **Query:** 
  ```promql
  (sum(rate(http_requests_total{job="demo-api-service",namespace="production",code=~"5.."}[5m])) / sum(rate(http_requests_total{job="demo-api-service",namespace="production"}[5m]))) * 100 > 5
  ```
- **Condition:** When `avg() of query A` is `above` 5
- **For duration:** 2 minutes
- **Severity:** critical

---

### Alert 4: SLO Violation - P95 Latency (>500ms for 5 minutes)

**Configuration:**
- **Alert name:** `SLO Violation - High P95 Latency`
- **Query:** 
  ```promql
  histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="demo-api-service",namespace="production"}[5m])) by (le)) * 1000 > 500
  ```
- **Condition:** When `avg() of query A` is `above` 500
- **For duration:** 5 minutes
- **Severity:** warning

---

### Alert 5: Service Down (Pod unavailable)

**Configuration:**
- **Alert name:** `Demo API Service Down`
- **Query:** 
  ```promql
  count(up{job="demo-api-service",namespace="production"} == 1) < 3
  ```
- **Condition:** When `count() of query A` is `below` 3
- **For duration:** 1 minute
- **Severity:** critical

---

## Quick Access

After creating these alerts:
1. Go to **Alerting → Alert rules** to see all configured alerts
2. Go to **Alerting → Notification policies** to configure alert routing
3. Go to **Alerting → Contact points** to add notification channels (email, Slack, PagerDuty, etc.)

## Testing Alerts

To trigger CPU alert:
```bash
kubectl exec -n production -it $(kubectl get pod -n production -l app=demo-api -o jsonpath='{.items[0].metadata.name}') -- sh -c "while true; do :; done"
```

To trigger error rate alert:
```bash
# Generate 500 errors
for i in {1..100}; do curl http://localhost:8080/error; done
```

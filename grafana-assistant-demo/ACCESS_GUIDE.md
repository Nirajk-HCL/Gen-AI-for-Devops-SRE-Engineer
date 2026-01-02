# Grafana Assistant Demo - Access Guide

## 🎉 Observability Stack Deployed Successfully!

### Access Information

**Grafana Dashboard**
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`
- (You'll be prompted to change password on first login - you can skip it)

**Prometheus**
- URL: http://localhost:9090
- No authentication required

**Sample Application**
- URL: http://localhost:8080
- Nginx web server for testing

**Node Exporter (System Metrics)**
- URL: http://localhost:9100/metrics
- Exposes system-level metrics

---

## 📊 What's Pre-Configured

### 1. Data Source
✅ Prometheus is automatically configured as the default datasource

### 2. Dashboard
✅ **System Monitoring Dashboard** is pre-loaded with:
   - CPU Usage (timeseries graph)
   - Memory Usage (timeseries graph)
   - Current CPU Usage (gauge)
   - Current Memory Usage (gauge)
   - Network Traffic (timeseries graph)
   - Disk Usage (timeseries graph)
   - System Uptime (stat)

### 3. Alert Rules (Prometheus)
✅ Four alert rules configured:
   - **HighCPUUsage**: Triggers when CPU > 80% for 5 minutes
   - **HighMemoryUsage**: Triggers when Memory > 85% for 5 minutes
   - **DiskSpaceLow**: Triggers when Disk > 90% for 10 minutes
   - **ServiceDown**: Triggers when service is unreachable for 1 minute

---

## 🚀 How to Use Grafana

### Step 1: Login to Grafana
1. Open http://localhost:3000 in your browser
2. Login with `admin` / `admin`
3. Click "Skip" when prompted to change password (or change it)

### Step 2: View Pre-Built Dashboard
1. Click on "Dashboards" icon (📊) in the left sidebar
2. Click "Browse"
3. You should see "System Monitoring Dashboard"
4. Click on it to view real-time metrics

### Step 3: Explore Prometheus Data
1. Click "Explore" icon (🧭) in the left sidebar
2. Select "Prometheus" datasource (already selected)
3. Try these PromQL queries:
   ```
   # CPU Usage
   100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
   
   # Memory Usage
   (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
   
   # Network Receive Rate
   rate(node_network_receive_bytes_total[5m])
   ```

### Step 4: Check Alerts
1. Go to http://localhost:9090 (Prometheus UI)
2. Click "Alerts" in the top menu
3. You'll see the 4 configured alert rules
4. Status will show "Inactive" (green) if thresholds are not breached

### Step 5: Create Your Own Dashboard
1. In Grafana, click "+" → "Create Dashboard"
2. Click "Add visualization"
3. Select "Prometheus" datasource
4. Use the "Code" mode and enter a PromQL query
5. Customize visualization type, colors, thresholds
6. Click "Apply" to add panel

### Step 6: Simulate Alert Triggering
To test CPU alert (WARNING: This will stress your system):
```powershell
# Run this in PowerShell to generate CPU load
1..4 | ForEach-Object { Start-Job { while($true) { $a = 1..10000 | % { [Math]::Sqrt($_) } } } }

# Wait 5 minutes, then check Prometheus alerts
# Stop the jobs when done:
Get-Job | Stop-Job
Get-Job | Remove-Job
```

---

## 🎯 Natural Language Queries (Simulated)

Since we don't have actual Grafana Assistant (requires Grafana Cloud), here's how it would work:

**Query:** *"Show me CPU usage"*
**Result:** Dashboard with CPU metrics from `node_cpu_seconds_total`

**Query:** *"Create an alert for high memory"*
**Result:** Alert rule for `node_memory_MemAvailable_bytes` with 85% threshold

**Query:** *"What's my system uptime?"*
**Result:** Panel showing `node_time_seconds - node_boot_time_seconds`

---

## 📚 Learn PromQL

### Basic Queries
```promql
# Instant vector - current value
node_memory_MemTotal_bytes

# Range vector - time series
node_cpu_seconds_total[5m]

# Rate calculation
rate(node_network_receive_bytes_total[5m])

# Aggregation
avg(node_load1)
sum(rate(node_cpu_seconds_total[5m])) by (cpu)

# Arithmetic
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

---

## 🛠️ Troubleshooting

**Grafana shows "No Data":**
- Check if Prometheus is running: http://localhost:9090
- Check Prometheus targets: http://localhost:9090/targets
- Ensure node-exporter is "UP"

**Can't access Grafana:**
- Check if container is running: `docker compose ps`
- Check logs: `docker compose logs grafana`
- Restart: `docker compose restart grafana`

**Metrics not showing:**
- Wait 30-60 seconds after startup
- Refresh Grafana page
- Check time range (default: Last 6 hours)

---

## 🔄 Stop/Start Services

```powershell
# Stop all services
cd D:\LAB\GENAI-Repo\GENAI\grafana-assistant-demo
docker compose down

# Start services
docker compose up -d

# View logs
docker compose logs -f grafana
docker compose logs -f prometheus

# Restart a single service
docker compose restart grafana
```

---

## 🎨 Customize Your Setup

### Add More Metrics
Edit `prometheus.yml` and add scrape targets:
```yaml
scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['my-app:8080']
```

### Create Custom Dashboards
1. Export from Grafana.com: https://grafana.com/grafana/dashboards/
2. Find Node Exporter dashboards (e.g., Dashboard ID: 1860)
3. Import in Grafana: Dashboards → Import → Enter ID: 1860

### Add Alertmanager
For actual alert notifications (email, Slack, PagerDuty):
1. Add alertmanager service to docker-compose.yml
2. Configure notification channels
3. Connect Prometheus to Alertmanager

---

## 📊 Demo Queries to Try

### System Performance
```promql
# CPU cores count
count(node_cpu_seconds_total{mode="idle"})

# Load average
node_load1

# Available memory in GB
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# Network bandwidth
sum(rate(node_network_receive_bytes_total[5m])) / 1024 / 1024
```

### Alerts Preview
```promql
# CPU usage (for alert)
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80

# Memory usage (for alert)
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
```

---

## 🎉 Enjoy Your Observability Stack!

You now have a fully functional Grafana + Prometheus setup with:
✅ Real-time system monitoring
✅ Pre-configured dashboards
✅ Alert rules ready to trigger
✅ Ability to create custom visualizations

**Next Steps:**
1. Explore the System Monitoring Dashboard
2. Try creating your own panels
3. Experiment with PromQL queries
4. Set up alert notifications

**For Grafana Cloud (with AI Assistant):**
Sign up at https://grafana.com/auth/sign-up/create-user

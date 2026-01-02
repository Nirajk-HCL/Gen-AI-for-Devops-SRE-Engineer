# Quick Verification Script
# Run this to verify all components are accessible

Write-Host "`n=== GRAFANA & PROMETHEUS VERIFICATION ===" -ForegroundColor Yellow
Write-Host ""

# Test 1: Grafana
Write-Host "[1/4] Testing Grafana..." -ForegroundColor Cyan
try {
    $grafana = Invoke-WebRequest -Uri "http://localhost:3000/api/health" -UseBasicParsing -TimeoutSec 5
    $health = ($grafana.Content | ConvertFrom-Json)
    if ($health.database -eq "ok") {
        Write-Host "  ✓ Grafana is running and healthy" -ForegroundColor Green
        Write-Host "    URL: http://localhost:3000" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ Grafana is not accessible" -ForegroundColor Red
    Write-Host "    Run: docker compose up -d" -ForegroundColor Yellow
}

# Test 2: Prometheus
Write-Host "`n[2/4] Testing Prometheus..." -ForegroundColor Cyan
try {
    $prom = Invoke-WebRequest -Uri "http://localhost:9090/-/healthy" -UseBasicParsing -TimeoutSec 5
    if ($prom.StatusCode -eq 200) {
        Write-Host "  ✓ Prometheus is running" -ForegroundColor Green
        Write-Host "    URL: http://localhost:9090" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ Prometheus is not accessible" -ForegroundColor Red
}

# Test 3: Alert Rules
Write-Host "`n[3/4] Checking Alert Rules..." -ForegroundColor Cyan
try {
    $rules = Invoke-WebRequest -Uri "http://localhost:9090/api/v1/rules" -UseBasicParsing -TimeoutSec 5
    $ruleData = ($rules.Content | ConvertFrom-Json).data.groups
    if ($ruleData.Count -gt 0) {
        Write-Host "  ✓ Alert rules loaded: $($ruleData.rules.Count) rules" -ForegroundColor Green
        $ruleData | ForEach-Object {
            Write-Host "    - $($_.name): $($_.rules.Count) rules" -ForegroundColor Gray
        }
        Write-Host "    View at: http://localhost:9090/alerts" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ Cannot fetch alert rules" -ForegroundColor Red
}

# Test 4: Dashboards
Write-Host "`n[4/4] Checking Grafana Dashboards..." -ForegroundColor Cyan
try {
    $dashboards = Invoke-WebRequest -Uri "http://localhost:3000/api/search?type=dash-db" `
        -UseBasicParsing -TimeoutSec 5 `
        -Headers @{Authorization = "Basic YWRtaW46YWRtaW4="} # admin:admin in base64
    $dashList = ($dashboards.Content | ConvertFrom-Json)
    if ($dashList.Count -gt 0) {
        Write-Host "  ✓ Dashboards available: $($dashList.Count)" -ForegroundColor Green
        $dashList | ForEach-Object {
            Write-Host "    - $($_.title)" -ForegroundColor Gray
        }
        Write-Host "    View at: http://localhost:3000/dashboards" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠ Cannot fetch dashboard list (authentication may be required)" -ForegroundColor Yellow
    Write-Host "    Login at: http://localhost:3000 (admin/admin)" -ForegroundColor Gray
}

# Summary
Write-Host "`n=== SUMMARY ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "  📊 Grafana:           http://localhost:3000" -ForegroundColor White
Write-Host "  🔔 Prometheus:        http://localhost:9090" -ForegroundColor White
Write-Host "  ⚠️  Alert Rules:       http://localhost:9090/alerts" -ForegroundColor White
Write-Host "  📈 Prometheus Graph:  http://localhost:9090/graph" -ForegroundColor White
Write-Host ""
Write-Host "Login Credentials:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  - TROUBLESHOOTING_GUIDE.md (complete access guide)" -ForegroundColor Gray
Write-Host "  - ALERT_CONFIGURATION_GUIDE.md (create Grafana alerts)" -ForegroundColor Gray
Write-Host "  - QUICK_REFERENCE.md (use case demonstration)" -ForegroundColor Gray
Write-Host ""

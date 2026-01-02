# Demo API Traffic Generator

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Demo API Traffic Generator" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting port-forward to demo-api service..." -ForegroundColor Yellow
Write-Host "Run this command in a separate terminal:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward -n production svc/demo-api 8081:8080" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter when port-forward is ready..." -ForegroundColor Yellow
Read-Host

Write-Host ""
Write-Host "Testing connectivity..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8081" -UseBasicParsing -TimeoutSec 5
    Write-Host "API is accessible!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Cannot reach API at localhost:8081" -ForegroundColor Red
    Write-Host "Make sure port-forward is running" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Generating traffic for 2 minutes..." -ForegroundColor Yellow
Write-Host "This will populate the Grafana dashboards with metrics" -ForegroundColor Gray
Write-Host ""

$endTime = (Get-Date).AddMinutes(2)
$requestCount = 0

while ((Get-Date) -lt $endTime) {
    try {
        $random = Get-Random -Minimum 1 -Maximum 100
        
        if ($random -le 90) {
            # 90% success rate
            $null = Invoke-WebRequest -Uri "http://localhost:8081/" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        } else {
            # 10% errors
            try {
                $null = Invoke-WebRequest -Uri "http://localhost:8081/timeout" -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop
            } catch {
                # Expected to fail
            }
        }
        
        $requestCount++

        if ($requestCount % 50 -eq 0) {
            Write-Host "  Generated $requestCount requests..." -ForegroundColor Gray
        }

        Start-Sleep -Milliseconds 100
    } catch {
        # Continue on errors
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Traffic generation complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total requests generated: $requestCount" -ForegroundColor White
Write-Host ""
Write-Host "Access Grafana dashboards at:" -ForegroundColor Yellow
Write-Host "  http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "View these dashboards:" -ForegroundColor Yellow
Write-Host "  1. API Service Monitoring" -ForegroundColor White
Write-Host "  2. API SLO Dashboard" -ForegroundColor White
Write-Host "  3. Incident Investigation Dashboard" -ForegroundColor White
Write-Host ""

# Screenshot Capture Guide

## 📸 Purpose
This guide helps ensure consistent, high-quality screenshots for all 7 use cases in the GenAI DevOps/SRE runbook documentation.

---

## 📋 Overview

### Total Screenshots Required: 80
- **Use Case 1:** 01-08 (8 screenshots)
- **Use Case 2:** 09-20 (12 screenshots)
- **Use Case 3:** 21-29 (9 screenshots)
- **Use Case 4:** 30-41 (12 screenshots)
- **Use Case 5:** 42-53 (12 screenshots)
- **Use Case 6:** 54-68 (15 screenshots)
- **Use Case 7:** 69-80 (12 screenshots)

### Storage Location
`D:\LAB\GENAI-Repo\GENAI\evidence\`

---

## 🛠️ Recommended Tools

### Option 1: Windows Snipping Tool (Built-in)
**Pros:** Free, built-in, simple
**Cons:** Manual process, no annotation features

**How to Use:**
1. Press `Windows + Shift + S`
2. Select area to capture
3. Click notification to open in Snipping Tool
4. Save as PNG with correct filename

### Option 2: ShareX (Recommended)
**Pros:** Free, powerful, auto-naming, annotations, upload
**Cons:** Requires installation

**Installation:**
```powershell
# Using Chocolatey
choco install sharex

# Or download from: https://getsharex.com/
```

**Configuration:**
1. Open ShareX
2. Task Settings → Capture → Screen capture → Active window
3. Task Settings → General → File naming → `evidence/{n2}-{y}{mo}{d}`
4. After capture settings → Upload image to... → Save image to file

### Option 3: Greenshot
**Pros:** Free, lightweight, easy annotations
**Cons:** Limited automation

**Installation:**
```powershell
choco install greenshot
```

---

## 📐 Technical Specifications

### Image Requirements
- **Format:** PNG (lossless compression)
- **Resolution:** 1920x1080 recommended (full HD)
- **DPI:** 96 DPI minimum
- **Color Depth:** 24-bit or 32-bit
- **File Size:** <2MB per screenshot (compress if needed)

### Naming Convention
```
XX-description.png
```
Where:
- `XX` = Two-digit sequential number (01-80)
- `description` = Short kebab-case description
- `.png` = File extension

**Examples:**
- `01-docker-version.png`
- `23-openai-validation.png`
- `54-grafana-directory.png`

---

## 📝 Capture Checklist by Use Case

### Use Case 1: Kubernetes Operations (01-08)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 01 | docker-version.png | `docker --version` output | Terminal |
| 02 | kind-cluster-creation.png | `kind create cluster` output | Terminal |
| 03 | kubectl-namespaces.png | `kubectl get namespaces` | Terminal |
| 04 | payment-deployment-yaml.png | deployment YAML file | Code Editor |
| 05 | payment-pods-running.png | `kubectl get pods` showing 3 pods | Terminal |
| 06 | frontend-pods-running.png | All 5 pods running | Terminal |
| 07 | pod-self-healing.png | Pod recreation after deletion | Terminal |
| 08 | all-pods-healthy.png | Final state - all healthy | Terminal |

### Use Case 2: Terraform IaC (09-20)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 09 | terraform-version.png | `terraform version` output | Terminal |
| 10 | main-tf-file.png | main.tf VPC configuration | Code Editor |
| 11 | variables-tf-file.png | variables.tf file | Code Editor |
| 12 | terraform-init.png | `terraform init` output | Terminal |
| 13 | terraform-validate.png | `terraform validate` success | Terminal |
| 14 | terraform-fmt.png | `terraform fmt` output | Terminal |
| 15 | staging-tfvars.png | staging.tfvars file | Code Editor |
| 16 | production-tfvars.png | production.tfvars file | Code Editor |
| 17 | terraform-plan-staging.png | Plan output for staging | Terminal |
| 18 | terraform-plan-production.png | Plan output for production | Terminal |
| 19 | resource-comparison.png | Side-by-side comparison | Screenshot |
| 20 | terraform-show-plan.png | Detailed plan output | Terminal |

### Use Case 3: Kube-Copilot (21-29)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 21 | kube-copilot-directory.png | Directory listing | Terminal |
| 22 | python-venv-created.png | Virtual env activation | Terminal |
| 23 | pip-install-dependencies.png | pip install output | Terminal |
| 24 | env-config.png | .env file contents | Code Editor |
| 25 | kubectl-verify-access.png | kubectl get pods output | Terminal |
| 26 | query-1-list-pods.png | AI response for query 1 | Terminal |
| 27 | query-2-check-issues.png | AI response for query 2 | Terminal |
| 28 | query-3-api-gateway.png | AI analysis of api-gateway | Terminal |
| 29 | query-4-resource-usage.png | Resource usage analysis | Terminal |

### Use Case 4: ArgoCD (30-41)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 30 | argocd-installation.png | `kubectl apply` ArgoCD | Terminal |
| 31 | argocd-pods-running.png | ArgoCD pods status | Terminal |
| 32 | argocd-port-forward.png | Port-forward command | Terminal |
| 33 | argocd-admin-password.png | Password retrieval | Terminal |
| 34 | argocd-ui-login.png | ArgoCD login page | Browser |
| 35 | app-manifests.png | Application YAML files | Code Editor |
| 36 | apps-deployed.png | `kubectl apply` output | Terminal |
| 37 | app-status.png | Application status list | Terminal |
| 38 | manual-sync.png | Manual sync in UI | Browser |
| 39 | self-healing.png | Self-healing demonstration | Terminal |
| 40 | out-of-sync.png | Out-of-sync state | Browser |
| 41 | rollback.png | Rollback operation | Browser |

### Use Case 5: MCP AWS (42-53)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 42 | mcp-aws-directory.png | Directory structure | Terminal |
| 43 | mcp-dependencies-install.png | pip install output | Terminal |
| 44 | config-yaml.png | config.yaml file | Code Editor |
| 45 | mcp-server-started.png | Server startup logs | Terminal |
| 46 | ec2-instance-created.png | EC2 creation JSON response | Terminal |
| 47 | ec2-list-instances.png | List instances output | Terminal |
| 48 | s3-bucket-created.png | S3 bucket creation response | Terminal |
| 49 | s3-file-uploaded.png | File upload response | Terminal |
| 50 | lambda-deployed.png | Lambda deployment response | Terminal |
| 51 | lambda-invoked.png | Lambda invocation result | Terminal |
| 52 | cloudwatch-metrics.png | CloudWatch metrics response | Terminal |
| 53 | cloudwatch-logs.png | CloudWatch logs response | Terminal |

### Use Case 6: Grafana (54-68)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 54 | grafana-directory.png | Directory listing | Terminal |
| 55 | docker-compose-yaml.png | docker-compose.yml file | Code Editor |
| 56 | docker-compose-up.png | docker-compose up output | Terminal |
| 57 | demo-api-port-forward.png | Port-forward for demo-api | Terminal |
| 58 | prometheus-targets.png | Prometheus targets page | Browser |
| 59 | generate-traffic.png | Traffic generation script | Terminal |
| 60 | grafana-ui-login.png | Grafana login page | Browser |
| 61 | dashboards-list.png | List of 4 dashboards | Browser |
| 62 | system-monitoring-dashboard.png | System dashboard with data | Browser |
| 63 | api-monitoring-dashboard.png | API dashboard with metrics | Browser |
| 64 | slo-dashboard.png | SLO dashboard | Browser |
| 65 | incident-dashboard.png | Incident investigation dashboard | Browser |
| 66 | alert-rules-yaml.png | alert_rules.yml file | Code Editor |
| 67 | prometheus-alerts.png | Prometheus alerts page | Browser |
| 68 | query-fix-comparison.png | Before/after query fix | Screenshot |

### Use Case 7: K8sGPT (69-80)

| # | Filename | Content | Type |
|---|----------|---------|------|
| 69 | k8sgpt-download.png | Downloaded k8sgpt.exe | Terminal |
| 70 | k8sgpt-version.png | k8sgpt version output | Terminal |
| 71 | cluster-access.png | kubectl cluster-info | Terminal |
| 72 | problematic-pods-yaml.png | problematic-pods.yaml file | Code Editor |
| 73 | test-pods-deployed.png | 5 pods in error states | Terminal |
| 74 | k8sgpt-basic-analysis.png | Basic analysis output | Terminal |
| 75 | openai-config.png | OpenAI auth configuration | Terminal |
| 76 | openai-validation.png | API key validation | Terminal |
| 77 | ai-enhanced-analysis.png | AI analysis with explanations | Terminal |
| 78 | comparison-table.png | Basic vs AI comparison | Screenshot |
| 79 | json-export.png | JSON export output | Terminal |
| 80 | docker-alternative.png | Docker k8sgpt command | Terminal |

---

## 🎨 Annotation Guidelines

### When to Annotate
- Highlight key information (error messages, success indicators)
- Point out specific UI elements
- Emphasize important values or states
- Draw attention to changes or differences

### Annotation Tools
- Red boxes for key areas
- Arrows pointing to important elements
- Text labels for clarification
- Green checkmarks for success
- Red X for errors

### Example Annotation Workflow (ShareX)
1. Capture screenshot
2. Image opens in ShareX editor automatically
3. Use tools:
   - Rectangle: Draw red box around key area
   - Arrow: Point to specific element
   - Text: Add label or note
   - Number: Add step numbers
4. Save annotated image

---

## 📏 Capture Best Practices

### Terminal Screenshots
1. **Set terminal to full screen** (F11 in PowerShell)
2. **Use high contrast theme** (easier to read)
3. **Increase font size** (16pt recommended)
4. **Clear previous output** (`cls` command)
5. **Show complete command and output**
6. **Wait for command to complete** before capturing
7. **Include prompt** (shows context and path)

### Browser Screenshots
1. **Use consistent browser** (Chrome or Edge)
2. **Zoom to 100%**
3. **Close unnecessary tabs**
4. **Show full page** (use F11 for fullscreen if needed)
5. **Wait for page to fully load**
6. **Disable browser extensions** (cleaner UI)
7. **Use incognito/private mode** (consistent appearance)

### Code Editor Screenshots
1. **Use consistent theme** (Dark+ or Light+)
2. **Show line numbers**
3. **Use syntax highlighting**
4. **Zoom to readable size** (14pt font)
5. **Show file name/path** in editor tab
6. **Collapse irrelevant sections**
7. **Highlight important lines** (selection or comments)

---

## 🔄 Capture Workflow

### Preparation Phase
1. ✅ Install capture tool (ShareX recommended)
2. ✅ Configure auto-naming: `evidence/XX-description.png`
3. ✅ Set save location: `D:\LAB\GENAI-Repo\GENAI\evidence\`
4. ✅ Test capture with dummy screenshot
5. ✅ Verify file saved correctly

### Execution Phase
For each use case:
1. 📖 Open runbook markdown file
2. 🔍 Identify screenshot reference (e.g., `evidence/01-docker-version.png`)
3. ⌨️ Execute corresponding command
4. ⏳ Wait for output to complete
5. 📸 Capture screenshot (Windows + Shift + S)
6. 🎨 Annotate if needed (red boxes, arrows)
7. 💾 Save with correct filename
8. ✔️ Verify image in evidence folder
9. ➡️ Move to next screenshot

### Verification Phase
1. ✅ Count total screenshots (should be 80)
2. ✅ Check naming convention (01-80, .png)
3. ✅ Verify file sizes (<2MB each)
4. ✅ Open random samples to check quality
5. ✅ Ensure all references in runbooks match files

---

## 🔍 Quality Checklist

### For Each Screenshot
- [ ] Clear and readable (no blur or pixelation)
- [ ] Correct filename (XX-description.png)
- [ ] Saved in evidence folder
- [ ] Shows complete command output (terminal)
- [ ] Full UI visible (browser/editor)
- [ ] Annotations helpful but not excessive
- [ ] File size reasonable (<2MB)
- [ ] No sensitive information visible (API keys, passwords)

### Common Issues to Avoid
- ❌ Blurry or low-resolution images
- ❌ Cut-off terminal output
- ❌ Wrong filename or numbering
- ❌ Saved in wrong folder
- ❌ Exposed API keys or secrets
- ❌ Inconsistent terminal theme
- ❌ Missing context (command not visible)
- ❌ Too much noise (unnecessary windows)

---

## 🚀 Quick Capture Scripts

### PowerShell Script to Check Progress
```powershell
# Check screenshot progress
$evidencePath = "D:\LAB\GENAI-Repo\GENAI\evidence"
$screenshots = Get-ChildItem -Path $evidencePath -Filter "*.png" | Sort-Object Name

Write-Host "Screenshot Capture Progress:"
Write-Host "============================="
Write-Host "Total screenshots: $($screenshots.Count) / 80"
Write-Host ""
Write-Host "Captured screenshots:"
$screenshots | ForEach-Object { Write-Host "✅ $($_.Name)" }

Write-Host ""
Write-Host "Missing screenshots:"
1..80 | ForEach-Object {
    $expected = "{0:D2}" -f $_
    $found = $screenshots | Where-Object { $_.Name -match "^$expected-" }
    if (-not $found) {
        Write-Host "❌ $expected-*.png"
    }
}
```

### Batch Screenshot Rename (if needed)
```powershell
# Rename screenshots to match convention
$evidencePath = "D:\LAB\GENAI-Repo\GENAI\evidence"
$files = Get-ChildItem -Path $evidencePath -Filter "*.png" | Sort-Object Name

$counter = 1
foreach ($file in $files) {
    $newName = "{0:D2}-{1}" -f $counter, $file.Name
    Rename-Item -Path $file.FullName -NewName $newName
    Write-Host "Renamed: $($file.Name) → $newName"
    $counter++
}
```

---

## 📊 Progress Tracking

Use this table to track capture progress:

| Use Case | Range | Total | Captured | Status |
|----------|-------|-------|----------|--------|
| 1. Kubernetes | 01-08 | 8 | 0 | ⏳ Pending |
| 2. Terraform | 09-20 | 12 | 0 | ⏳ Pending |
| 3. Troubleshooting | 21-29 | 9 | 0 | ⏳ Pending |
| 4. ArgoCD | 30-41 | 12 | 0 | ⏳ Pending |
| 5. MCP AWS | 42-53 | 12 | 0 | ⏳ Pending |
| 6. Grafana | 54-68 | 15 | 0 | ⏳ Pending |
| 7. K8sGPT | 69-80 | 12 | 0 | ⏳ Pending |
| **TOTAL** | **01-80** | **80** | **0** | **0%** |

Legend:
- ⏳ Pending
- 🔄 In Progress
- ✅ Complete

---

## 🆘 Troubleshooting

### Issue: Screenshot Too Large (>2MB)
**Solution:**
```powershell
# Compress PNG using ImageMagick
magick convert input.png -quality 85 output.png

# Or use online tool: https://tinypng.com/
```

### Issue: Wrong Terminal Font/Theme
**Solution:**
```powershell
# PowerShell: Set font to Consolas 16pt
# Terminal → Settings → Profiles → Default → Appearance
# Font face: Consolas
# Font size: 16
# Color scheme: One Half Dark
```

### Issue: Browser Screenshots Show Personal Data
**Solution:**
- Use incognito/private mode
- Clear bookmarks bar
- Hide browser extensions
- Use test account credentials

### Issue: Can't Capture Full Terminal Output
**Solution:**
```powershell
# Increase buffer size
# Terminal → Settings → Profiles → Default → Advanced
# History size: 9999

# Or redirect to file first
kubectl get pods > output.txt
Get-Content output.txt
# Then capture
```

---

## 📚 Additional Resources

- [ShareX Documentation](https://getsharex.com/docs/)
- [Greenshot Documentation](https://getgreenshot.org/help/)
- [Windows Snipping Tool Guide](https://support.microsoft.com/en-us/windows/use-snipping-tool-to-capture-screenshots-00246869-1843-655f-f220-97299b865f6b)
- [PNG Optimization Tools](https://tinypng.com/)

---

**Last Updated:** January 1, 2026  
**Version:** 1.0.0  
**Status:** ✅ Complete guide ready for screenshot capture

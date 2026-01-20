# Deploy script pro Kubernetes (Windows PowerShell)

param(
    [string]$GitHubUsername,
    [string]$GitHubToken
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Guestbook App - Kubernetes Deployment" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Ověření prerequisites
Write-Host "`nKontrolování prerequisites..." -ForegroundColor Yellow

$prerequisites = @('kubectl', 'docker')
foreach ($cmd in $prerequisites) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Write-Host "✓ $cmd" -ForegroundColor Green
    } else {
        Write-Host "❌ $cmd není nainstalován" -ForegroundColor Red
        exit 1
    }
}

# Dotaz na GitHub username a token
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Zadejte GitHub username"
}

if (-not $GitHubToken) {
    $GitHubToken = Read-Host "Zadejte GitHub token" -AsSecureString
    $GitHubToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($GitHubToken))
}

# Přihlášení do registry
Write-Host "`nPřihlášení do GitHub Container Registry..." -ForegroundColor Yellow
$GitHubToken | docker login ghcr.io -u $GitHubUsername --password-stdin
Write-Host "✓ Přihlášení úspěšné" -ForegroundColor Green

# Build Docker image
Write-Host "`nBuildování Docker image..." -ForegroundColor Yellow
$ImageName = "ghcr.io/$GitHubUsername/guestbook-app:latest"
docker build -f Dockerfile -t $ImageName .
Write-Host "✓ Image vytvořen: $ImageName" -ForegroundColor Green

# Push do registry
Write-Host "`nPush do registry..." -ForegroundColor Yellow
docker push $ImageName
Write-Host "✓ Push úspěšný" -ForegroundColor Green

# Úprava deployment.yaml
Write-Host "`nÚprava deployment.yaml..." -ForegroundColor Yellow
$deploymentPath = "k8s\deployment.yaml"
$deploymentContent = Get-Content $deploymentPath -Raw
$deploymentContent = $deploymentContent -replace "ghcr.io/YOUR_USERNAME/os-projekt:latest", $ImageName
Set-Content $deploymentPath $deploymentContent
Write-Host "✓ deployment.yaml upraven" -ForegroundColor Green

# Vytvoření namespace
Write-Host "`nVytvoření namespace..." -ForegroundColor Yellow
kubectl create namespace guestbook --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✓ Namespace vytvořen" -ForegroundColor Green

# Aplikování manifests
Write-Host "`nAplikování Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
Write-Host "✓ Manifests aplikovány" -ForegroundColor Green

# Čekání na deployment
Write-Host "`nČekání na nasazení podů..." -ForegroundColor Yellow
kubectl rollout status deployment/guestbook-app -n guestbook --timeout=300s
Write-Host "✓ Deployment hotov" -ForegroundColor Green

# Zobrazení informací
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Nasazení bylo úspěšné!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nInformace:" -ForegroundColor Yellow
kubectl get pods -n guestbook
Write-Host ""
kubectl get svc -n guestbook
Write-Host ""

Write-Host "Přístup k aplikaci:" -ForegroundColor Yellow
Write-Host "kubectl port-forward -n guestbook svc/guestbook-service 8000:80"
Write-Host "http://localhost:8000"

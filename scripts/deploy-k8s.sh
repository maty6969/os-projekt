#!/bin/bash
# Deploy script pro Kubernetes

set -e

# Barvy pro výstup
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Guestbook App - Kubernetes Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Ověření prerequisites
echo -e "\n${YELLOW}Kontrola prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl není nainstalován${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker není nainstalován${NC}"
    exit 1
fi

echo -e "${GREEN}✓ kubectl${NC}"
echo -e "${GREEN}✓ Docker${NC}"

# Dotaz na GitHub username
read -p "Zadejte GitHub username: " GITHUB_USERNAME
read -p "Zadejte GitHub token: " GITHUB_TOKEN

# Přihlášení do registry
echo -e "\n${YELLOW}Přihlášení do GitHub Container Registry...${NC}"
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
echo -e "${GREEN}✓ Přihlášení úspěšné${NC}"

# Build Docker image
echo -e "\n${YELLOW}Buildování Docker image...${NC}"
IMAGE_NAME="ghcr.io/$GITHUB_USERNAME/guestbook-app:latest"
docker build -f Dockerfile -t $IMAGE_NAME .
echo -e "${GREEN}✓ Image vytvořen: $IMAGE_NAME${NC}"

# Push do registry
echo -e "\n${YELLOW}Push do registry...${NC}"
docker push $IMAGE_NAME
echo -e "${GREEN}✓ Push úspěšný${NC}"

# Úprava deployment.yaml
echo -e "\n${YELLOW}Úprava deployment.yaml...${NC}"
sed -i "s|ghcr.io/YOUR_USERNAME/os-projekt:latest|$IMAGE_NAME|g" k8s/deployment.yaml
echo -e "${GREEN}✓ deployment.yaml upraven${NC}"

# Vytvoření namespace
echo -e "\n${YELLOW}Vytvoření namespace...${NC}"
kubectl create namespace guestbook --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace vytvořen${NC}"

# Aplikování manifests
echo -e "\n${YELLOW}Aplikování Kubernetes manifests...${NC}"
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
echo -e "${GREEN}✓ Manifests aplikovány${NC}"

# Čekání na deployment
echo -e "\n${YELLOW}Čekání na nasazení podů...${NC}"
kubectl rollout status deployment/guestbook-app -n guestbook --timeout=300s
echo -e "${GREEN}✓ Deployment hotov${NC}"

# Zobrazení informací
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Nasazení bylo úspěšné!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Informace:${NC}"
kubectl get pods -n guestbook
echo ""
kubectl get svc -n guestbook
echo ""

echo -e "${YELLOW}Přístup k aplikaci:${NC}"
echo -e "kubectl port-forward -n guestbook svc/guestbook-service 8000:80"
echo -e "http://localhost:8000"

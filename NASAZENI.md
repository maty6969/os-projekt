# POSTUP NASAZENÍ - Návod k odevzdání

## 1. GitHub Setup

### Krok 1: Vytvoření repozitáře na GitHubu

1. Přejděte na https://github.com/new
2. Zadejte jméno: `guestbook-app` (nebo `os-projekt`)
3. Zvolte `Public` (školitel si bude moci prohlédnout)
4. **NEKLIKEJTE** "Initialize with README" (už máme soubory)
5. Klikněte "Create repository"

### Krok 2: Upload na GitHub

```bash
cd "c:\Users\matej\skola\os-projekt\guestbook-app"

# Přidejte remote URL (nahraďte YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/guestbook-app.git

# Připravte hlavní větev (pro novější Git)
git branch -M main

# Pushněte kód
git push -u origin main
```

### Krok 3: Nastavení GitHub Actions

1. Jděte na váš repozitář
2. Klikněte "Actions"
3. Měl by se zobrazit workflow "Build and Push Docker Image"
4. Potvrďte, že workflow běží

**GitHub Actions nyní automaticky:**
- Buildí Docker image na každý push
- Pushuje do GitHub Container Registry
- Tagi jsou `latest`, `main`, `sha-xxx`

## 2. Docker Registry

### Přihlášení do GitHub Container Registry

```bash
# Vytvořte Personal Access Token na https://github.com/settings/tokens
# Scope: write:packages, read:packages

# Přihlášení (v PowerShell)
$token = Read-Host "GitHub Token" -AsSecureString
$tokenPlainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($token))

# Přihlášení
echo $tokenPlainText | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

## 3. Kubernetes Nasazení (SSPU Opava Rancher)

### Příprava

1. Přihlaste se na: https://rancher.kube.sspu-opava.cz
2. Vyberte váš projekt/cluster

### Krok 1: Úprava deployment.yaml

Editujte `k8s/deployment.yaml`:

```yaml
# Najděte řádek:
image: ghcr.io/YOUR_USERNAME/os-projekt:latest

# Nahraďte YOUR_USERNAME vaším GitHub username
```

### Krok 2: Nasazení přes Rancher UI

```bash
# Nebo použijte kubectl (pokud máte nainstalovaný)
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml -n guestbook
```

**V Rancher UI:**
1. Jděte na "Workloads" → "Deployments"
2. Klikněte "Import YAML"
3. Vložte obsah `k8s/deployment.yaml`
4. Klikněte "Create"

### Krok 3: Ověření nasazení

```bash
# Zkontrolujte pody
kubectl get pods -n guestbook

# Zkontrolujte service
kubectl get svc -n guestbook

# Prohledy logů
kubectl logs -n guestbook -l app=guestbook
```

### Krok 4: Přístup k aplikaci

V Rancher:
1. Jděte na "Service Discovery" → "Services"
2. Najděte `guestbook-service`
3. Klikněte na IP/DNS název pro přístup

Nebo přes port-forward:
```bash
kubectl port-forward -n guestbook svc/guestbook-service 8000:80
```

Aplikace bude dostupná na `http://localhost:8000`

## 4. Odevzdání

Pošlete do MS Teams:

### Zpráva s informacemi:

```
Guestbook Web Application - Odevzdání

🔗 GitHub Repozitář: https://github.com/YOUR_USERNAME/guestbook-app

📦 Docker Image: ghcr.io/YOUR_USERNAME/guestbook-app:latest

☸️  Kubernetes Info:
- Namespace: guestbook
- Service: guestbook-service
- Deployment: guestbook-app
- Replicas: 2 (HPA: 2-5)

✅ Implementované funkce:
✓ Flask webová aplikace
✓ SQLAlchemy ORM s dvěma tabulkami (Users, Messages)
✓ Responsivní design s externím CSS
✓ Validace formulářů a sanitizace vstupu
✓ XSS ochrana a bezpečnost
✓ Docker a docker-compose
✓ GitHub Actions pro automatické buildění
✓ Kubernetes manifest s deployment, service, HPA, ingress
✓ .gitignore a .env.example
✓ Dokumentace v README

🔐 Bezpečnost:
- Odstranění XSS útoků
- SQL Injection ochrana přes ORM
- Validace emailu a délky zprávy
- Sanitizace HTML vstupu
- CSRF ochrana
```

## 5. Lokální Testování

Před odevzdáním si otestujte:

```bash
# Instalace
pip install -r requirements.txt

# Spuštění (s SQLite pro testování)
python run.py

# Navštivte http://localhost:5000
```

## 6. Troubleshooting

### Chyba: "pyodbc" - SQL Server driver not found
**Řešení:** Pro lokální testování použijte SQLite. Upravte .env:
```env
DATABASE_URL=sqlite:///guestbook.db
```

### Chyba: "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

### Docker build fail
```bash
docker build -t guestbook:latest -f Dockerfile ./
```

### Kubernetes chyba
```bash
# Zkontrolujte image
kubectl describe pod -n guestbook [POD_NAME]

# Zkontrolujte event
kubectl describe deployment -n guestbook guestbook-app
```

## 📚 Dokumentace

- [Flask Dokumentace](https://flask.palletsprojects.com/)
- [SQLAlchemy Dokumentace](https://docs.sqlalchemy.org/)
- [Kubernetes Dokumentace](https://kubernetes.io/docs/)
- [GitHub Actions Dokumentace](https://docs.github.com/en/actions)

---

**Kontakt a podpora:** Prosíme, obrátěte se na školitele, pokud máte problémy.

# 🎓 GUESTBOOK WEB APP - FINÁLNÍ NÁVOD K ODEVZDÁNÍ

**Školní projekt pro SSPU Opava - Leden 2026**

---

## 📋 Co bylo vytvořeno

Kompletní webová aplikace **"Kniha návštěv"** s těmito komponentami:

### ✅ Backend (Flask + SQLAlchemy)
- Dvě databázové tabulky: **Users** (autoři) a **Messages** (zprávy)
- Vztah N:1 - jeden uživatel může napsat více zpráv
- RESTful API s validací dat
- Bezpečnostní prvky (XSS ochrana, CSRF, SQL Injection ochrana)
- Stránkování zpráv (10 na stránku)

### ✅ Frontend (HTML/CSS/JavaScript)
- Responzivní design (desktop, tablet, mobil)
- Externí CSS soubor (`style.css`)
- Makra v Jinja2 templates
- Validace formulářů klient-side + server-side
- Bezpečnostní prvky (sanitizace, escape)

### ✅ Databáze
- SQL Server (pro produkci)
- SQLite (pro vývoj - bez SQL Serveru)
- Automatické vytváření tabulek
- Migrační skript připraven

### ✅ Docker & Containerizace
- `Dockerfile` (multi-stage build)
- `docker-compose.yml` (s SQL Server pro vývoj)
- `.dockerignore` pro optimalizaci
- GitHub Actions pro automatické buildění

### ✅ Kubernetes & Orchestrace
- `k8s/deployment.yaml` (s HPA, Network Policy, PDB)
- `k8s/ingress.yaml` (pro veřejný přístup)
- Health checks (liveness + readiness probes)
- Resource limits a requests

### ✅ CI/CD
- GitHub Actions workflow
- Automatické buildění Docker image
- Publikace do GitHub Container Registry

### ✅ Bezpečnost
- `.gitignore` - nezapisuje hesla, .env soubory
- `.env.example` - šablona pro konfiguraci
- Sanitizace vstupu - XSS ochrana
- Validace email a délky zprávy
- Bezpečné uložení tajemství

---

## 🚀 QUICK START - Jak začít

### 1. Klonování a Instalace

```bash
cd c:\Users\matej\skola\os-projekt\guestbook-app

# Vytvoření virtuálního prostředí
python -m venv venv
venv\Scripts\activate

# Instalace závislostí
pip install -r requirements.txt

# Kopírování .env šablony
copy .env.example .env
```

### 2. Spuštění Lokálně (s SQLite)

```bash
# Upravte .env:
# DATABASE_URL=sqlite:///guestbook.db

# Spuštění aplikace
python run.py

# Otevřete http://localhost:5000
```

### 3. Spuštění s Docker

```bash
# Build image
docker build -t guestbook:latest .

# Spuštění s SQL Server
docker-compose up -d

# Přístup: http://localhost:5000
```

---

## 📤 ODEVZDÁNÍ NA GITHUB

### Krok 1: Vytvoření GitHub Repozitáře

1. Přejděte na https://github.com/new
2. **Repository name**: `guestbook-app`
3. **Public** (školitel si bude moci prohlédnout kód)
4. **NEPOUŽÍVEJTE** "Initialize with README"
5. Klikněte **Create repository**

### Krok 2: Upload Kódu

```bash
cd "c:\Users\matej\skola\os-projekt\guestbook-app"

# Přidejte remote (nahraďte YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/guestbook-app.git

# Změna názvu branch
git branch -M main

# Upload na GitHub
git push -u origin main
```

### Krok 3: Ověření GitHub Actions

1. Přejděte na váš repozitář
2. Klikněte na **Actions**
3. Měl by být workflow **"Build and Push Docker Image"**
4. Workflow by měl automaticky běžet

**Výsledek:** Docker image je automaticky buildován a publikován do GitHub Container Registry

📍 **URL vašeho image:**
```
ghcr.io/YOUR_USERNAME/guestbook-app:latest
```

---

## ☸️ NASAZENÍ NA KUBERNETES (Rancher)

### Krok 1: Příprava

1. Přihlaste se do Rancher: https://rancher.kube.sspu-opava.cz
2. Vyberte svůj projekt/cluster

### Krok 2: Úprava deployment.yaml

Otevřete `k8s/deployment.yaml` a nahraďte:

```yaml
# Najděte:
image: ghcr.io/YOUR_USERNAME/os-projekt:latest

# Změňte na:
image: ghcr.io/YOUR_USERNAME/guestbook-app:latest
```

### Krok 3: Nasazení přes Rancher UI

**Možnost A: Rancher GUI**
1. Jděte na **Workloads** → **Deployments**
2. Klikněte **Create from YAML**
3. Vložte obsah `k8s/deployment.yaml`
4. Klikněte **Create**

**Možnost B: kubectl (pokud máte)** 
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml -n guestbook
```

### Krok 4: Ověření Nasazení

```bash
# Zkontrolujte pody
kubectl get pods -n guestbook

# Zkontrolujte service
kubectl get svc -n guestbook

# Prohledy logů
kubectl logs -n guestbook -l app=guestbook
```

### Krok 5: Přístup k Aplikaci

V Rancher:
- Jděte na **Service Discovery** → **Services** 
- Najděte `guestbook-service`
- Klikněte na **88.25.x.x** (veřejná IP/DNS)

Nebo přes port-forward:
```bash
kubectl port-forward -n guestbook svc/guestbook-service 8000:80
```

Aplikace bude na: **http://localhost:8000**

---

## 📨 ODEVZDÁNÍ - CO POSLAT DO TEAMS

### Zpráva s následujícím:

```
═══════════════════════════════════════════════════════════
🎓 GUESTBOOK WEB APPLICATION - ODEVZDÁNÍ
═══════════════════════════════════════════════════════════

🔗 GitHub Repozitář:
https://github.com/YOUR_USERNAME/guestbook-app

📦 Docker Image:
ghcr.io/YOUR_USERNAME/guestbook-app:latest

☸️ Kubernetes Nasazení:
- Namespace: guestbook
- Deployment: guestbook-app
- Service: guestbook-service
- Replicas: 2 (HPA 2-5)
- URL: http://[IP_Z_RANCHER]

═══════════════════════════════════════════════════════════

✅ IMPLEMENTOVANÉ POŽADAVKY:

1. Web Aplikace:
   ✓ Flask framework
   ✓ SQLAlchemy ORM
   ✓ Dvě tabulky (Users + Messages)
   ✓ Vztah N:1

2. Frontend:
   ✓ Responzivní design
   ✓ Externí CSS (style.css)
   ✓ Makra v templates
   ✓ Validace formulářů
   ✓ Safe_characters a sanitizace

3. Databáze:
   ✓ SQL Server (produkce)
   ✓ SQLite (vývoj)
   ✓ Verzování schématu

4. GitHub:
   ✓ Public repozitář
   ✓ .gitignore (bez hesel)
   ✓ .env.example
   ✓ README.md

5. Docker:
   ✓ Dockerfile (multi-stage)
   ✓ docker-compose.yml
   ✓ GitHub Actions workflow
   ✓ Automatické buildění

6. Kubernetes:
   ✓ deployment.yaml
   ✓ service
   ✓ HPA (Horizontal Pod Autoscaler)
   ✓ Health checks
   ✓ Resource limits
   ✓ Network Policy

7. Bezpečnost:
   ✓ XSS ochrana
   ✓ CSRF ochrana
   ✓ SQL Injection ochrana
   ✓ Input validation
   ✓ Error handling

═══════════════════════════════════════════════════════════
```

---

## 🔍 STRUKTURA SOUBORU

```
guestbook-app/
├── app/                      # Flask aplikace
│   ├── __init__.py          # Inicializace aplikace
│   ├── models.py            # SQLAlchemy modely (Users, Messages)
│   ├── routes.py            # Flask routy
│   ├── utils.py             # Validace, sanitizace
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Základní template
│   │   ├── index.html       # Domovská stránka
│   │   ├── add_message.html # Formulář
│   │   └── user_messages.html
│   └── static/              # Statické soubory
│       └── css/
│           └── style.css    # Styly
│
├── k8s/                     # Kubernetes manifesty
│   ├── deployment.yaml      # Deployment + Service + HPA
│   └── ingress.yaml         # Ingress controller
│
├── scripts/                 # Nasazovací skriptu
│   ├── deploy-k8s.sh       # Linux/Mac
│   └── deploy-k8s.ps1      # Windows PowerShell
│
├── .github/                # GitHub Actions
│   └── workflows/
│       └── docker-build.yml # CI/CD workflow
│
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python závislosti
├── run.py                  # Hlavní skript
├── .env.example            # Šablona .env
├── .gitignore              # Git ignorování
├── README.md               # Dokumentace
├── NASAZENI.md             # Návod na nasazení
└── SQLITE_VYVOJ.md         # SQLite pro vývoj
```

---

## 🐛 ŘEŠENÍ PROBLÉMU

### Chyba: "Module 'pyodbc' not found"
```bash
# Řešení: Použijte SQLite pro vývoj
# Upravte .env: DATABASE_URL=sqlite:///guestbook.db
```

### Chyba: "Databáze neexistuje"
```bash
# Aplikace ji automaticky vytvoří při spuštění
python run.py
```

### Docker image se nebuildi
```bash
# Zkuste s explicitním path
docker build -f Dockerfile -t guestbook:latest ./
```

### Kubernetes pod se nespouští
```bash
# Zkontrolujte logy
kubectl logs -n guestbook -l app=guestbook

# Zkontrolujte events
kubectl describe pod -n guestbook <POD_NAME>
```

---

## 📚 UŽITEČNÉ REFERENCE

- 🔗 [Flask](https://flask.palletsprojects.com/)
- 🔗 [SQLAlchemy](https://docs.sqlalchemy.org/)
- 🔗 [Docker](https://docs.docker.com/)
- 🔗 [Kubernetes](https://kubernetes.io/docs/)
- 🔗 [GitHub Actions](https://docs.github.com/en/actions)
- 🔗 [Rancher](https://rancher.com/docs/)

---

## 📝 CHECKLIST PŘED ODEVZDÁNÍM

- [ ] Kód je na GitHubu
- [ ] GitHub Actions běží a builduje image
- [ ] Docker image je na ghcr.io
- [ ] k8s/deployment.yaml je upraven s vaším username
- [ ] Aplikace je nasazená na Kubernetes (Rancher)
- [ ] Aplikace je dostupná na URL z Rancher
- [ ] Kód je commitnut a pushnut
- [ ] .env.example obsahuje šablonu (bez hesel)
- [ ] README.md je kompletní
- [ ] Zpráva s detaily poslána do Teams

---

**Hotovo! 🎉 Projekt je připraven k odevzdání.**

Pokud máte jakékoli problémy, kontaktujte svého školitele nebo se podívejte do dokumentace.

Hodně štěstí! 💪

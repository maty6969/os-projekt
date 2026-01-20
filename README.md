# 📖 Guestbook Web Application

Jednoduchá webová aplikace knihy návštěv vytvořená v Flaskuuses. Aplikace umožňuje uživatelům přidat své jméno, email a zprávu, kterou si mohou ostatní prohlédnout.

## Funkce

- ✅ Přidávání zpráv s validací formuláře
- ✅ Bezpečné uložení dat do SQL Server
- ✅ Responsivní design s moderním CSS
- ✅ Dvě tabulky: Users (autoři) a Messages (zprávy)
- ✅ Vztah mezi tabulkami (user → více zpráv)
- ✅ Stránkování zpráv
- ✅ Ochrana před XSS útoky
- ✅ Docker a Kubernetes support
- ✅ GitHub Actions pro automatické buildení

## Architektura

### Databázový model

```
Users (autoři)
├── id (PK)
├── name (VARCHAR)
├── email (VARCHAR, unique)
└── created_at (DATETIME)

Messages (zprávy)
├── id (PK)
├── user_id (FK → users.id)
├── message (TEXT)
└── created_at (DATETIME)
```

### Struktura projektu

```
guestbook-app/
├── app/
│   ├── __init__.py          # Flask aplikace
│   ├── models.py            # SQLAlchemy modely
│   ├── routes.py            # Flask routy
│   ├── utils.py             # Validace a sanitizace
│   ├── static/
│   │   └── css/
│   │       └── style.css    # Styly
│   └── templates/
│       ├── base.html        # Základní template
│       ├── index.html       # Domovská stránka
│       ├── add_message.html # Formulář
│       └── user_messages.html
├── k8s/
│   ├── deployment.yaml
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       └── docker-build.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── run.py
```

## Instalace

### Lokálně (bez SQL Server)

```bash
# Klonování repozitáře
git clone https://github.com/YOUR_USERNAME/guestbook-app.git
cd guestbook-app

# Vytvoření virtuálního prostředí
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows

# Instalace závislostí
pip install -r requirements.txt

# Nastavení prostředí
cp .env.example .env
# Upravte .env podle potřeby

# Spuštění aplikace
python run.py
```

Aplikace bude dostupná na `http://localhost:5000`

### S Docker Compose

```bash
# Nastavení prostředí
cp .env.example .env

# Spuštění aplikace s SQL Server
docker-compose up -d

# Migrace databáze (pokud je potřeba)
docker-compose exec app python run.py

# Zastavení aplikace
docker-compose down
```

## Nasazení na Kubernetes

### Příprava

1. Vytvořte účet na [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

2. Upravte `k8s/deployment.yaml`:
   - Nahraďte `YOUR_USERNAME` vaším GitHub username
   - Nastavte správné环境 proměnné

3. Vytvořte secret s databází:

```bash
kubectl create secret generic guestbook-secrets \
  --from-literal=SECRET_KEY='your-secret-key' \
  --from-literal=DATABASE_URL='your-db-url' \
  -n guestbook
```

### Nasazení

```bash
# Nasazení aplikace
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Ověření nasazení
kubectl get pods -n guestbook
kubectl get svc -n guestbook

# Prohledy logů
kubectl logs -n guestbook -l app=guestbook

# Port forwarding (pro testování)
kubectl port-forward -n guestbook svc/guestbook-service 8000:80
```

Aplikace bude dostupná na `http://guestbook.example.com` (po nastavení DNS)

## Validace a Bezpečnost

- **Sanitizace vstupu**: Odstranění nebezpečných HTML a skriptů
- **Validace email**: Kontrola formátu emailu
- **Délka zprávy**: 5-1000 znaků
- **XSS ochrana**: HTML escapování všech uživatelských vstupů
- **CSRF ochrana**: Flask session management
- **SQL Injection ochrana**: SQLAlchemy ORM

## Prostředí

Vytvořte `.env` soubor na základě `.env.example`:

```env
# Databáze (SQL Server)
DATABASE_URL=mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=guestbook;Trusted_Connection=yes;

# Flask
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-min-32-chars

# Server
PORT=5000
HOST=0.0.0.0
```

## GitHub Actions

Automatické buildění Docker image:
- Triggeruje se na push do `main` nebo `develop` větví
- Buildí Docker image a pushuje do GitHub Container Registry
- Tagi jsou automaticky generovány

Obrazy najdete na: `ghcr.io/YOUR_USERNAME/os-projekt`

## Příklady použití

### Přidání zprávy přes cURL

```bash
curl -X POST http://localhost:5000/add-message \
  -d "name=Jan&email=jan@example.com&message=Zdravím z Pythonu!"
```

### Zobrazení zpráv ze specifického uživatele

```
http://localhost:5000/user/1
```

## Licencování

Projekt je pod licencí MIT.

## Podpora

Pro hlášení chyb a připomínek prosím vytvořte Issue na GitHubu.

---

**Školní projekt pro SSPU Opava**
Vytvořeno: Leden 2026

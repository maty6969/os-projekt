# Alternatíva pro lokální vývoj - SQLite

Pokud nemáte nainstalovaný SQL Server a chcete vyvíjet lokálně, můžete použít SQLite.

## Instalace

```bash
pip install flask-sqlalchemy
```

SQLite je již součástí Pythonu, není třeba nic instalovat.

## Úprava konfigurace

Upravte `app/__init__.py`:

```python
# Nahraďte řádek:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=guestbook;Trusted_Connection=yes;'
)

# Tímto:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///guestbook.db'
)
```

## Spuštění

```bash
# Upravte .env
DATABASE_URL=sqlite:///guestbook.db

# Spusťte aplikaci
python run.py

# Databáze bude automaticky vytvořena v guestbook.db
```

## Poznámka pro produkci

Pro produkci v Kubernetes MUSÍ být použitý SQL Server!

Upravte `k8s/deployment.yaml` a ujistěte se, že `DATABASE_URL` ukazuje na SQL Server.

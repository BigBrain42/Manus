# 🚀 Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
python main.py
```

Öffnen Sie: http://localhost:8000/docs

## Erste Schritte

### 1. Alle Benutzer abrufen
```bash
curl http://localhost:8000/api/users
```

### 2. Neuen Benutzer erstellen
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max Mustermann",
    "email": "max@example.com",
    "bio": "Ich bin Max",
    "avatar_url": "https://example.com/avatar.jpg"
  }'
```

### 3. Python-Skript ausführen
```python
from utils import get_all_records, create_user

# Alle Benutzer abrufen
users = get_all_records("users")
print(f"Benutzer: {len(users)}")

# Neuen Benutzer erstellen
user = create_user("Max", "max@example.com")
print(f"Erstellt: {user['id']}")
```

## Dokumentation

- [PYTHON_EXAMPLES.md](PYTHON_EXAMPLES.md) - Python-Beispiele
- [SQL_EXAMPLES.md](SQL_EXAMPLES.md) - SQL-Abfragen
- [JAVA_EXAMPLES.md](JAVA_EXAMPLES.md) - Java-Integration

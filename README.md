# Supabase Python Backend API

Ein vollständiges, produktionsreifes System mit Python-Backend (FastAPI) und modernem Frontend für die Integration mit Supabase. Dieses Projekt bietet eine benutzerfreundliche Weboberfläche und eine vollständige REST-API mit Beispielen für SQL, Python und Java.

## 🚀 Quick Start

### Automatisch (empfohlen)

**Linux/macOS:**
```bash
cd /home/ubuntu/supabase-backend-api
./start.sh
```

**Windows:**
```bash
cd supabase-backend-api
start.bat
```

### Manuell

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Backend starten
python main.py

# In neuem Terminal: Frontend starten
cd frontend
python -m http.server 5000
```

### Zugriff

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Dokumentation**: http://localhost:8000/docs

## 📚 Dokumentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Vollständiger Anfänger-Guide (HIER STARTEN!)
- **[QUICK_START.md](QUICK_START.md)** - 5-Minuten-Guide für Anfänger
- **[PYTHON_EXAMPLES.md](PYTHON_EXAMPLES.md)** - 50+ Python-Code-Beispiele
- **[SQL_EXAMPLES.md](SQL_EXAMPLES.md)** - 30+ SQL-Abfrage-Beispiele
- **[JAVA_EXAMPLES.md](JAVA_EXAMPLES.md)** - Java-Integration-Beispiele

## 🎨 Frontend Features

Das Frontend bietet eine moderne, benutzerfreundliche Oberfläche mit:

- **Dashboard** mit Statistiken und Schnellzugriff
- **Benutzerverwaltung** - Erstellen, Anzeigen, Löschen
- **Produktverwaltung** - Erstellen, Anzeigen, Löschen
- **Bestellungsverwaltung** - Erstellen, Anzeigen, Löschen
- **Suchfunktion** für alle Tabellen
- **Responsive Design** für alle Geräte
- **Toast-Benachrichtigungen** für Benutzer-Feedback

## 🔗 API Endpoints

Die API bietet vollständige CRUD-Operationen für Benutzer, Produkte und Bestellungen. Alle Endpoints sind unter http://localhost:8000/docs dokumentiert und testbar.

| Ressource | GET | POST | PUT | DELETE |
|-----------|-----|------|-----|--------|
| `/api/users` | ✓ | ✓ | ✓ | ✓ |
| `/api/products` | ✓ | ✓ | ✓ | ✓ |
| `/api/orders` | ✓ | ✓ | ✓ | ✓ |
| `/api/query/user-orders/{id}` | ✓ | - | - | - |
| `/api/query/user-products/{id}` | ✓ | - | - | - |

## 📁 Projektstruktur

```
supabase-backend-api/
├── main.py                    # FastAPI Backend
├── utils.py                   # Python Hilfsfunktionen
├── requirements.txt           # Abhängigkeiten
├── .env                       # Supabase Konfiguration
├── start.sh                   # Startup Script (Linux/macOS)
├── start.bat                  # Startup Script (Windows)
├── README.md                  # Diese Datei
├── GETTING_STARTED.md         # Anfänger-Guide
├── QUICK_START.md             # 5-Minuten-Guide
├── PYTHON_EXAMPLES.md         # Python Beispiele
├── SQL_EXAMPLES.md            # SQL Abfragen
├── JAVA_EXAMPLES.md           # Java Integration
└── frontend/
    ├── index.html             # Hauptseite
    ├── css/
    │   └── style.css          # Styling
    └── js/
        ├── api.js             # API Client
        └── app.js             # Anwendungslogik
```

## 📖 Weitere Ressourcen

- [Supabase Dokumentation](https://supabase.com/docs)
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Python Dokumentation](https://docs.python.org/)

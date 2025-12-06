# Python Beispiele für Supabase

## Basis-Operationen

### Alle Datensätze abrufen
```python
from utils import get_all_records

users = get_all_records("users")
for user in users:
    print(f"- {user['name']} ({user['email']})")
```

### Einen Datensatz nach ID abrufen
```python
from utils import get_record_by_id

user = get_record_by_id("users", 1)
if user:
    print(f"Gefunden: {user['name']}")
```

### Nach Filter suchen
```python
from utils import get_records_by_filter

admins = get_records_by_filter("users", "role", "admin")
print(f"Admin-Benutzer: {len(admins)}")
```

### Datensatz einfügen
```python
from utils import insert_record

user_data = {
    "name": "Max Mustermann",
    "email": "max@example.com",
    "bio": "Ich bin Max",
    "role": "consumer",
    "isActive": True
}
new_user = insert_record("users", user_data)
print(f"Erstellt: {new_user['id']}")
```

### Datensatz aktualisieren
```python
from utils import update_record

updated = update_record(1, {"name": "Neuer Name", "bio": "Neue Biografie"})
print(f"Aktualisiert: {updated['name']}")
```

### Datensatz löschen
```python
from utils import delete_record

if delete_record("users", 1):
    print("Benutzer gelöscht")
```

## Benutzer-Operationen

### Benutzer nach E-Mail suchen
```python
from utils import get_user_by_email

user = get_user_by_email("max@example.com")
if user:
    print(f"Gefunden: {user['name']}")
```

### Neuen Benutzer erstellen
```python
from utils import create_user

user = create_user("Max Mustermann", "max@example.com", "Ich bin Max")
print(f"Erstellt: {user['id']}")
```

### Benutzerprofil aktualisieren
```python
from utils import update_user_profile

updated = update_user_profile(1, name="Neuer Name", bio="Neue Biografie")
print(f"Aktualisiert: {updated['name']}")
```

## Produkt-Operationen

### Produkte eines Besitzers abrufen
```python
from utils import get_products_by_owner

products = get_products_by_owner(1)
for product in products:
    print(f"- {product['name']}: {product['price']}€")
```

### Neues Produkt erstellen
```python
from utils import create_product

product = create_product(
    name="Laptop",
    price=999.99,
    owner_id=1,
    description="Ein leistungsstarker Laptop"
)
print(f"Erstellt: {product['id']}")
```

## Bestellungs-Operationen

### Bestellungen eines Benutzers abrufen
```python
from utils import get_user_orders

orders = get_user_orders(1)
print(f"Bestellungen: {len(orders)}")
```

### Neue Bestellung erstellen
```python
from utils import create_order

order = create_order(
    user_id=1,
    product_id=5,
    quantity=2,
    total_price=1999.98
)
print(f"Erstellt: {order['id']}")
```

### Bestellungsstatus aktualisieren
```python
from utils import update_order_status

updated = update_order_status(1, "completed")
print(f"Status: {updated['status']}")
```

## Statistiken

### Datensätze zählen
```python
from utils import count_records

total_users = count_records("users")
total_products = count_records("products")
total_orders = count_records("orders")

print(f"Benutzer: {total_users}")
print(f"Produkte: {total_products}")
print(f"Bestellungen: {total_orders}")
```

### Benutzerstatistiken
```python
from utils import get_user_statistics

stats = get_user_statistics(1)
print(f"Benutzer: {stats['user']['name']}")
print(f"Bestellungen: {stats['total_orders']}")
print(f"Gesamtausgaben: {stats['total_orders_value']}€")
print(f"Produkte: {stats['total_products']}")
```

### Gesamtbestellwert
```python
from utils import get_total_orders_value

total = get_total_orders_value()
print(f"Gesamtumsatz: {total}€")
```

## Fehlerbehandlung

```python
from utils import get_user_by_email

try:
    user = get_user_by_email("max@example.com")
    if user:
        print(f"Gefunden: {user['name']}")
    else:
        print("Benutzer nicht gefunden")
except Exception as e:
    print(f"Fehler: {str(e)}")
```

## Batch-Operationen

```python
from utils import insert_record

users_data = [
    {"name": "User 1", "email": "user1@example.com"},
    {"name": "User 2", "email": "user2@example.com"},
    {"name": "User 3", "email": "user3@example.com"},
]

for user_data in users_data:
    insert_record("users", user_data)
    print(f"Erstellt: {user_data['name']}")
```

## Vollständiges Beispiel-Skript

```python
#!/usr/bin/env python3

from utils import (
    get_all_records,
    create_user,
    get_user_by_email,
    count_records,
    get_user_statistics
)

def main():
    print("=== Supabase Python Beispiele ===\n")
    
    # 1. Alle Benutzer abrufen
    print("1. Alle Benutzer:")
    users = get_all_records("users", limit=5)
    for user in users:
        print(f"   - {user['name']} ({user['email']})")
    print()
    
    # 2. Statistiken
    print("2. Statistiken:")
    print(f"   Benutzer: {count_records('users')}")
    print(f"   Produkte: {count_records('products')}")
    print(f"   Bestellungen: {count_records('orders')}")
    print()
    
    # 3. Benutzer nach E-Mail suchen
    print("3. Benutzer suchen:")
    user = get_user_by_email("max@example.com")
    if user:
        print(f"   Gefunden: {user['name']}")
    else:
        print("   Nicht gefunden")
    print()

if __name__ == "__main__":
    main()
```

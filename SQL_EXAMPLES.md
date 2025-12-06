# SQL Beispiele für Supabase

## Benutzer-Operationen

### Alle Benutzer abrufen
```sql
SELECT * FROM users;
```

### Benutzer nach Rolle filtern
```sql
SELECT * FROM users WHERE role = 'admin';
```

### Benutzer nach E-Mail suchen
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

### Neuen Benutzer erstellen
```sql
INSERT INTO users (name, email, bio, avatar, role, isActive)
VALUES ('Max Mustermann', 'max@example.com', 'Ich bin Max', 'https://example.com/avatar.jpg', 'consumer', true);
```

### Benutzerprofil aktualisieren
```sql
UPDATE users 
SET name = 'Neuer Name', bio = 'Neue Biografie'
WHERE id = 1;
```

### Benutzer löschen
```sql
DELETE FROM users WHERE id = 1;
```

### Benutzer nach Erstellungsdatum sortieren
```sql
SELECT * FROM users ORDER BY createdAt DESC LIMIT 10;
```

## Produkt-Operationen

### Alle Produkte abrufen
```sql
SELECT * FROM products;
```

### Produkte eines Besitzers
```sql
SELECT * FROM products WHERE ownerId = 1;
```

### Produkte nach Preis filtern
```sql
SELECT * FROM products WHERE price > 50 AND price < 200;
```

### Neues Produkt erstellen
```sql
INSERT INTO products (name, description, price, ownerId, image, isActive)
VALUES ('Laptop', 'Ein leistungsstarker Laptop', 999.99, 1, 'https://example.com/laptop.jpg', true);
```

### Produktpreis aktualisieren
```sql
UPDATE products 
SET price = 1299.99, description = 'Aktualisierte Beschreibung'
WHERE id = 1;
```

### Produkte nach Preis sortieren
```sql
SELECT * FROM products ORDER BY price DESC;
```

## Bestellungs-Operationen

### Alle Bestellungen abrufen
```sql
SELECT * FROM orders;
```

### Bestellungen eines Benutzers
```sql
SELECT * FROM orders WHERE userId = 1;
```

### Bestellungen nach Status filtern
```sql
SELECT * FROM orders WHERE status = 'completed';
```

### Neue Bestellung erstellen
```sql
INSERT INTO orders (userId, productId, quantity, totalPrice, status)
VALUES (1, 5, 2, 1999.98, 'pending');
```

### Bestellungsstatus aktualisieren
```sql
UPDATE orders 
SET status = 'completed'
WHERE id = 1;
```

## Komplexe Abfragen

### Bestellungen mit Details
```sql
SELECT 
    o.id,
    o.quantity,
    o.totalPrice,
    o.status,
    u.name as user_name,
    p.name as product_name,
    p.price as product_price
FROM orders o
JOIN users u ON o.userId = u.id
JOIN products p ON o.productId = p.id
ORDER BY o.createdAt DESC;
```

### Produkte, die am häufigsten bestellt wurden
```sql
SELECT 
    p.id,
    p.name,
    COUNT(o.id) as order_count,
    SUM(o.quantity) as total_quantity
FROM products p
JOIN orders o ON p.id = o.productId
GROUP BY p.id, p.name
ORDER BY order_count DESC
LIMIT 10;
```

### Benutzer mit den meisten Bestellungen
```sql
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.totalPrice) as total_spent
FROM users u
JOIN orders o ON u.id = o.userId
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;
```

## Aggregationen und Statistiken

### Gesamtzahl der Benutzer
```sql
SELECT COUNT(*) as total_users FROM users;
```

### Gesamtwert aller Bestellungen
```sql
SELECT SUM(totalPrice) as total_revenue FROM orders;
```

### Durchschnittlicher Bestellwert
```sql
SELECT AVG(totalPrice) as avg_order_value FROM orders;
```

### Benutzer nach Rolle zählen
```sql
SELECT role, COUNT(*) as count FROM users GROUP BY role;
```

### Bestellungen nach Status zählen
```sql
SELECT status, COUNT(*) as count FROM orders GROUP BY status;
```

### Umsatz nach Benutzer
```sql
SELECT 
    u.name,
    COUNT(o.id) as orders,
    SUM(o.totalPrice) as revenue
FROM users u
LEFT JOIN orders o ON u.id = o.userId
GROUP BY u.id, u.name
ORDER BY revenue DESC;
```

## Tipps für Anfänger

**Immer WHERE verwenden**: Verwenden Sie WHERE-Klauseln, um versehentliche Massenänderungen zu vermeiden.

**Backup vor Änderungen**: Führen Sie vor großen Änderungen ein SELECT durch, um die betroffenen Datensätze zu überprüfen.

**Joins verstehen**: Verwenden Sie INNER JOIN, LEFT JOIN, RIGHT JOIN je nach Anforderung.

**Aggregationen**: GROUP BY und Aggregationsfunktionen (COUNT, SUM, AVG) sind mächtige Werkzeuge.

## Häufige Fehler vermeiden

❌ **Falsch**: `DELETE FROM users;` (löscht alle Benutzer!)

✅ **Richtig**: `DELETE FROM users WHERE id = 1;`

❌ **Falsch**: `UPDATE products SET price = 0;` (setzt alle Preise auf 0!)

✅ **Richtig**: `UPDATE products SET price = 99.99 WHERE id = 1;`

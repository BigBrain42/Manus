"""
Supabase Utility Functions
Hilfsfunktionen für häufige Datenbankoperationen
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# ============================================================================
# Allgemeine Datenbankoperationen
# ============================================================================

def get_all_records(table_name: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Alle Datensätze aus einer Tabelle abrufen"""
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"Fehler beim Abrufen von {table_name}: {str(e)}")
        return []


def get_record_by_id(table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
    """Einen Datensatz nach ID abrufen"""
    try:
        response = supabase.table(table_name).select("*").eq("id", record_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Fehler beim Abrufen von {table_name} mit ID {record_id}: {str(e)}")
        return None


def get_records_by_filter(table_name: str, filter_column: str, filter_value: Any) -> List[Dict[str, Any]]:
    """Datensätze nach einem Filter abrufen"""
    try:
        response = supabase.table(table_name).select("*").eq(filter_column, filter_value).execute()
        return response.data
    except Exception as e:
        print(f"Fehler beim Filtern von {table_name}: {str(e)}")
        return []


def insert_record(table_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Einen neuen Datensatz einfügen"""
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Fehler beim Einfügen in {table_name}: {str(e)}")
        return None


def update_record(table_name: str, record_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Einen Datensatz aktualisieren"""
    try:
        response = supabase.table(table_name).update(data).eq("id", record_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Fehler beim Aktualisieren von {table_name}: {str(e)}")
        return None


def delete_record(table_name: str, record_id: int) -> bool:
    """Einen Datensatz löschen"""
    try:
        supabase.table(table_name).delete().eq("id", record_id).execute()
        return True
    except Exception as e:
        print(f"Fehler beim Löschen aus {table_name}: {str(e)}")
        return False


# ============================================================================
# Benutzer-spezifische Funktionen
# ============================================================================

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Benutzer nach E-Mail abrufen"""
    users = get_records_by_filter("users", "email", email)
    return users[0] if users else None


def create_user(name: str, email: str, bio: str = None, avatar_url: str = None) -> Optional[Dict[str, Any]]:
    """Einen neuen Benutzer erstellen"""
    user_data = {
        "name": name,
        "email": email,
        "bio": bio,
        "avatar": avatar_url,
    }
    return insert_record("users", user_data)


def update_user_profile(user_id: int, name: str = None, bio: str = None, avatar_url: str = None) -> Optional[Dict[str, Any]]:
    """Benutzerprofil aktualisieren"""
    update_data = {}
    if name:
        update_data["name"] = name
    if bio:
        update_data["bio"] = bio
    if avatar_url:
        update_data["avatar"] = avatar_url
    
    return update_record("users", user_id, update_data)


# ============================================================================
# Produkt-spezifische Funktionen
# ============================================================================

def get_products_by_owner(owner_id: int) -> List[Dict[str, Any]]:
    """Alle Produkte eines Besitzers abrufen"""
    return get_records_by_filter("products", "ownerId", owner_id)


def create_product(name: str, price: float, owner_id: int, description: str = None, image_url: str = None) -> Optional[Dict[str, Any]]:
    """Ein neues Produkt erstellen"""
    product_data = {
        "name": name,
        "price": price,
        "ownerId": owner_id,
        "description": description,
        "image": image_url,
    }
    return insert_record("products", product_data)


# ============================================================================
# Bestellungs-spezifische Funktionen
# ============================================================================

def get_user_orders(user_id: int) -> List[Dict[str, Any]]:
    """Alle Bestellungen eines Benutzers abrufen"""
    return get_records_by_filter("orders", "userId", user_id)


def create_order(user_id: int, product_id: int, quantity: int, total_price: float) -> Optional[Dict[str, Any]]:
    """Eine neue Bestellung erstellen"""
    order_data = {
        "userId": user_id,
        "productId": product_id,
        "quantity": quantity,
        "totalPrice": total_price,
        "status": "pending",
    }
    return insert_record("orders", order_data)


def update_order_status(order_id: int, status: str) -> Optional[Dict[str, Any]]:
    """Status einer Bestellung aktualisieren"""
    return update_record("orders", order_id, {"status": status})


# ============================================================================
# Statistik- und Analysefunktionen
# ============================================================================

def count_records(table_name: str) -> int:
    """Anzahl der Datensätze in einer Tabelle zählen"""
    try:
        response = supabase.table(table_name).select("id", count="exact").execute()
        return response.count or 0
    except Exception as e:
        print(f"Fehler beim Zählen von {table_name}: {str(e)}")
        return 0


def get_total_orders_value() -> float:
    """Gesamtwert aller Bestellungen berechnen"""
    try:
        orders = get_all_records("orders", limit=1000)
        return sum(order.get("totalPrice", 0) for order in orders)
    except Exception as e:
        print(f"Fehler beim Berechnen der Gesamtbestellungen: {str(e)}")
        return 0.0


def get_user_statistics(user_id: int) -> Dict[str, Any]:
    """Statistiken für einen Benutzer abrufen"""
    user = get_record_by_id("users", user_id)
    orders = get_user_orders(user_id)
    products = get_products_by_owner(user_id)
    
    total_orders_value = sum(order.get("totalPrice", 0) for order in orders)
    
    return {
        "user": user,
        "total_orders": len(orders),
        "total_orders_value": total_orders_value,
        "total_products": len(products),
        "orders": orders,
        "products": products,
    }

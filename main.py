"""
Supabase FastAPI Backend
Ein modernes Python-Backend für die Supabase-Integration mit FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Laden Sie Umgebungsvariablen
load_dotenv()

# FastAPI App initialisieren
app = FastAPI(
    title="Supabase Backend API",
    description="Python Backend für Supabase-Integration",
    version="1.0.0"
)

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Client initialisieren
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL und SUPABASE_ANON_KEY müssen in .env definiert sein")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# ============================================================================
# Pydantic Models für Datenvalidierung
# ============================================================================

class UserProfile(BaseModel):
    """Modell für Benutzerprofil"""
    id: Optional[int] = None
    name: str
    email: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class Product(BaseModel):
    """Modell für Produkt"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    owner_id: int


class Order(BaseModel):
    """Modell für Bestellung"""
    id: Optional[int] = None
    user_id: int
    product_id: int
    quantity: int
    total_price: float


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Überprüfen Sie die API-Gesundheit"""
    return {
        "status": "healthy",
        "message": "Supabase Backend läuft",
        "supabase_connected": True
    }


@app.get("/")
async def root():
    """Willkommensnachricht"""
    return {
        "message": "Willkommen zum Supabase FastAPI Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "users": "/api/users",
            "products": "/api/products",
            "orders": "/api/orders"
        }
    }


# ============================================================================
# User Endpoints
# ============================================================================

@app.get("/api/users")
async def get_users(limit: int = 10):
    """Alle Benutzer abrufen"""
    try:
        response = supabase.table("users").select("*").limit(limit).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """Einen bestimmten Benutzer abrufen"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
        return {"success": True, "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/users")
async def create_user(user: UserProfile):
    """Einen neuen Benutzer erstellen"""
    try:
        user_data = {
            "name": user.name,
            "email": user.email,
            "bio": user.bio,
            "avatar": user.avatar_url,
        }
        response = supabase.table("users").insert(user_data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user: UserProfile):
    """Einen Benutzer aktualisieren"""
    try:
        user_data = {
            "name": user.name,
            "email": user.email,
            "bio": user.bio,
            "avatar": user.avatar_url,
        }
        response = supabase.table("users").update(user_data).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    """Einen Benutzer löschen"""
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return {"success": True, "message": "Benutzer gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Product Endpoints
# ============================================================================

@app.get("/api/products")
async def get_products(limit: int = 10):
    """Alle Produkte abrufen"""
    try:
        response = supabase.table("products").select("*").limit(limit).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Ein bestimmtes Produkt abrufen"""
    try:
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
        return {"success": True, "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/products")
async def create_product(product: Product):
    """Ein neues Produkt erstellen"""
    try:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "ownerId": product.owner_id,
        }
        response = supabase.table("products").insert(product_data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: Product):
    """Ein Produkt aktualisieren"""
    try:
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        response = supabase.table("products").update(product_data).eq("id", product_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    """Ein Produkt löschen"""
    try:
        response = supabase.table("products").delete().eq("id", product_id).execute()
        return {"success": True, "message": "Produkt gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Order Endpoints
# ============================================================================

@app.get("/api/orders")
async def get_orders(limit: int = 10):
    """Alle Bestellungen abrufen"""
    try:
        response = supabase.table("orders").select("*").limit(limit).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    """Eine bestimmte Bestellung abrufen"""
    try:
        response = supabase.table("orders").select("*").eq("id", order_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Bestellung nicht gefunden")
        return {"success": True, "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/orders")
async def create_order(order: Order):
    """Eine neue Bestellung erstellen"""
    try:
        order_data = {
            "userId": order.user_id,
            "productId": order.product_id,
            "quantity": order.quantity,
            "totalPrice": order.total_price,
            "status": "pending",
        }
        response = supabase.table("orders").insert(order_data).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    """Eine Bestellung aktualisieren"""
    try:
        order_data = {
            "quantity": order.quantity,
            "totalPrice": order.total_price,
        }
        response = supabase.table("orders").update(order_data).eq("id", order_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Bestellung nicht gefunden")
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/orders/{order_id}")
async def delete_order(order_id: int):
    """Eine Bestellung löschen"""
    try:
        response = supabase.table("orders").delete().eq("id", order_id).execute()
        return {"success": True, "message": "Bestellung gelöscht"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Custom Query Endpoints
# ============================================================================

@app.get("/api/query/user-orders/{user_id}")
async def get_user_orders(user_id: int):
    """Alle Bestellungen eines Benutzers abrufen"""
    try:
        response = supabase.table("orders").select("*").eq("userId", user_id).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/query/user-products/{user_id}")
async def get_user_products(user_id: int):
    """Alle Produkte eines Benutzers abrufen"""
    try:
        response = supabase.table("products").select("*").eq("ownerId", user_id).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

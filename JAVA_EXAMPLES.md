# Java Beispiele für Supabase

## Maven Dependencies

```xml
<dependencies>
    <dependency>
        <groupId>com.squareup.okhttp3</groupId>
        <artifactId>okhttp</artifactId>
        <version>4.11.0</version>
    </dependency>
    
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.10.1</version>
    </dependency>
</dependencies>
```

## Basis-Setup

```java
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import com.google.gson.Gson;

public class SupabaseClient {
    private static final String SUPABASE_URL = "https://uxvpsvbhsftgvqfaqlbp.supabase.co";
    private static final String SUPABASE_KEY = "your_anon_key";
    
    private OkHttpClient httpClient = new OkHttpClient();
    private Gson gson = new Gson();
    
    public String makeRequest(String endpoint) throws Exception {
        String url = SUPABASE_URL + "/rest/v1/" + endpoint;
        
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + SUPABASE_KEY)
            .addHeader("apikey", SUPABASE_KEY)
            .get()
            .build();
        
        Response response = httpClient.newCall(request).execute();
        return response.body().string();
    }
}
```

## Benutzer-Operationen

### Alle Benutzer abrufen
```java
public List<User> getAllUsers() throws Exception {
    String response = makeRequest("users?limit=100");
    User[] users = gson.fromJson(response, User[].class);
    return Arrays.asList(users);
}
```

### Neuen Benutzer erstellen
```java
public User createUser(String name, String email) throws Exception {
    JsonObject userJson = new JsonObject();
    userJson.addProperty("name", name);
    userJson.addProperty("email", email);
    userJson.addProperty("role", "consumer");
    
    String response = makePostRequest("users", userJson.toString());
    User[] users = gson.fromJson(response, User[].class);
    return users.length > 0 ? users[0] : null;
}
```

## User Model

```java
public class User {
    private int id;
    private String name;
    private String email;
    private String role;
    private String bio;
    private String avatar;
    
    // Getter und Setter
    public int getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public String getRole() { return role; }
    
    @Override
    public String toString() {
        return "User{" + "id=" + id + ", name='" + name + '\'' + '}';
    }
}
```

## Produkt-Operationen

### Produkte eines Besitzers
```java
public List<Product> getProductsByOwner(int ownerId) throws Exception {
    String response = makeRequest("products?ownerId=eq." + ownerId);
    Product[] products = gson.fromJson(response, Product[].class);
    return Arrays.asList(products);
}
```

### Neues Produkt erstellen
```java
public Product createProduct(String name, double price, int ownerId) throws Exception {
    JsonObject productJson = new JsonObject();
    productJson.addProperty("name", name);
    productJson.addProperty("price", price);
    productJson.addProperty("ownerId", ownerId);
    
    String response = makePostRequest("products", productJson.toString());
    Product[] products = gson.fromJson(response, Product[].class);
    return products.length > 0 ? products[0] : null;
}
```

## Bestellungs-Operationen

### Bestellungen eines Benutzers
```java
public List<Order> getUserOrders(int userId) throws Exception {
    String response = makeRequest("orders?userId=eq." + userId);
    Order[] orders = gson.fromJson(response, Order[].class);
    return Arrays.asList(orders);
}
```

### Neue Bestellung erstellen
```java
public Order createOrder(int userId, int productId, int quantity, double totalPrice) throws Exception {
    JsonObject orderJson = new JsonObject();
    orderJson.addProperty("userId", userId);
    orderJson.addProperty("productId", productId);
    orderJson.addProperty("quantity", quantity);
    orderJson.addProperty("totalPrice", totalPrice);
    orderJson.addProperty("status", "pending");
    
    String response = makePostRequest("orders", orderJson.toString());
    Order[] orders = gson.fromJson(response, Order[].class);
    return orders.length > 0 ? orders[0] : null;
}
```

## Vollständiges Beispiel

```java
public class SupabaseExample {
    public static void main(String[] args) {
        try {
            SupabaseClient client = new SupabaseClient();
            
            // Alle Benutzer abrufen
            List<User> users = client.getAllUsers();
            System.out.println("Benutzer gefunden: " + users.size());
            
            for (User user : users) {
                System.out.println("- " + user.getName() + " (" + user.getEmail() + ")");
            }
            
            // Neuen Benutzer erstellen
            User newUser = client.createUser("Max Mustermann", "max@example.com");
            if (newUser != null) {
                System.out.println("Neuer Benutzer: " + newUser.getId());
            }
            
        } catch (Exception e) {
            System.err.println("Fehler: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

## Fehlerbehandlung

```java
public User getUserSafe(int userId) {
    try {
        String response = makeRequest("users?id=eq." + userId);
        User[] users = gson.fromJson(response, User[].class);
        return users.length > 0 ? users[0] : null;
    } catch (Exception e) {
        System.err.println("Fehler beim Abrufen des Benutzers: " + e.getMessage());
        return null;
    }
}
```

## Tipps für Java-Entwickler

Verwenden Sie Pojo-Klassen mit Getter/Setter für Daten. Behandeln Sie immer Exceptions bei API-Aufrufen. Nutzen Sie Gson für JSON-Serialisierung/Deserialisierung. OkHttp ist eine robuste Bibliothek für HTTP-Requests. Verwenden Sie SLF4J für strukturiertes Logging.

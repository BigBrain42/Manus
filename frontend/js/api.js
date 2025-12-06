/**
 * API Client für Supabase Backend
 * Kommuniziert mit dem Python FastAPI Backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

class APIClient {
    /**
     * Macht einen HTTP-Request zum Backend
     */
    static async request(method, endpoint, data = null) {
        const url = `${API_BASE_URL}${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ========== USER ENDPOINTS ==========

    static async getUsers(limit = 100) {
        return this.request('GET', `/users?limit=${limit}`);
    }

    static async getUser(userId) {
        return this.request('GET', `/users/${userId}`);
    }

    static async createUser(name, email, bio = '', avatarUrl = '') {
        const data = {
            name: name,
            email: email,
            bio: bio,
            avatar_url: avatarUrl
        };
        return this.request('POST', '/users', data);
    }

    static async updateUser(userId, name, email, bio = '', avatarUrl = '') {
        const data = {
            name: name,
            email: email,
            bio: bio,
            avatar_url: avatarUrl
        };
        return this.request('PUT', `/users/${userId}`, data);
    }

    static async deleteUser(userId) {
        return this.request('DELETE', `/users/${userId}`);
    }

    // ========== PRODUCT ENDPOINTS ==========

    static async getProducts(limit = 100) {
        return this.request('GET', `/products?limit=${limit}`);
    }

    static async getProduct(productId) {
        return this.request('GET', `/products/${productId}`);
    }

    static async createProduct(name, price, ownerId, description = '') {
        const data = {
            name: name,
            price: price,
            owner_id: ownerId,
            description: description
        };
        return this.request('POST', '/products', data);
    }

    static async updateProduct(productId, name, price, description = '') {
        const data = {
            name: name,
            price: price,
            description: description
        };
        return this.request('PUT', `/products/${productId}`, data);
    }

    static async deleteProduct(productId) {
        return this.request('DELETE', `/products/${productId}`);
    }

    // ========== ORDER ENDPOINTS ==========

    static async getOrders(limit = 100) {
        return this.request('GET', `/orders?limit=${limit}`);
    }

    static async getOrder(orderId) {
        return this.request('GET', `/orders/${orderId}`);
    }

    static async createOrder(userId, productId, quantity, totalPrice) {
        const data = {
            user_id: userId,
            product_id: productId,
            quantity: quantity,
            total_price: totalPrice
        };
        return this.request('POST', '/orders', data);
    }

    static async updateOrder(orderId, quantity, totalPrice) {
        const data = {
            quantity: quantity,
            total_price: totalPrice
        };
        return this.request('PUT', `/orders/${orderId}`, data);
    }

    static async deleteOrder(orderId) {
        return this.request('DELETE', `/orders/${orderId}`);
    }

    // ========== QUERY ENDPOINTS ==========

    static async getUserOrders(userId) {
        return this.request('GET', `/query/user-orders/${userId}`);
    }

    static async getUserProducts(userId) {
        return this.request('GET', `/query/user-products/${userId}`);
    }
}

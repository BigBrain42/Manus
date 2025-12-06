/**
 * Supabase Backend - Frontend Application
 * Hauptanwendungslogik
 */

// ========== INITIALIZATION ==========

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDashboard();
});

function setupEventListeners() {
    // Navigation Links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            switchPage(page);
        });
    });
}

// ========== PAGE NAVIGATION ==========

function switchPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected page
    const pageElement = document.getElementById(`${page}-page`);
    if (pageElement) {
        pageElement.classList.add('active');
    }

    // Set active nav link
    const navLink = document.querySelector(`[data-page="${page}"]`);
    if (navLink) {
        navLink.classList.add('active');
    }

    // Load page data
    switch (page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'users':
            loadUsers();
            break;
        case 'products':
            loadProducts();
            break;
        case 'orders':
            loadOrders();
            break;
    }
}

// ========== DASHBOARD ==========

async function loadDashboard() {
    try {
        // Load statistics
        const usersResponse = await APIClient.getUsers(1000);
        const productsResponse = await APIClient.getProducts(1000);
        const ordersResponse = await APIClient.getOrders(1000);

        const users = usersResponse.data || [];
        const products = productsResponse.data || [];
        const orders = ordersResponse.data || [];

        // Calculate revenue
        const revenue = orders.reduce((sum, order) => sum + (order.totalPrice || 0), 0);

        // Update stats
        document.getElementById('stat-users').textContent = users.length;
        document.getElementById('stat-products').textContent = products.length;
        document.getElementById('stat-orders').textContent = orders.length;
        document.getElementById('stat-revenue').textContent = '€' + revenue.toFixed(2);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Fehler beim Laden des Dashboards', 'error');
    }
}

// ========== USERS ==========

async function loadUsers() {
    try {
        const response = await APIClient.getUsers();
        const users = response.data || [];

        const usersList = document.getElementById('users-list');
        
        if (users.length === 0) {
            usersList.innerHTML = '<div class="loading">Keine Benutzer gefunden</div>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>E-Mail</th>
                        <th>Rolle</th>
                        <th>Status</th>
                        <th>Aktionen</th>
                    </tr>
                </thead>
                <tbody>
        `;

        users.forEach(user => {
            const status = user.isActive ? '✓ Aktiv' : '✗ Inaktiv';
            html += `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.name || '-'}</td>
                    <td>${user.email || '-'}</td>
                    <td><span class="badge">${user.role || 'user'}</span></td>
                    <td>${status}</td>
                    <td>
                        <button class="btn btn-danger btn-small" onclick="deleteUser(${user.id})">
                            <i class="fas fa-trash"></i> Löschen
                        </button>
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        usersList.innerHTML = html;
    } catch (error) {
        console.error('Error loading users:', error);
        showToast('Fehler beim Laden der Benutzer', 'error');
    }
}

function showUserModal() {
    document.getElementById('user-modal').classList.add('show');
}

function closeUserModal() {
    document.getElementById('user-modal').classList.remove('show');
    document.getElementById('user-form').reset();
}

async function submitUserForm(event) {
    event.preventDefault();

    const name = document.getElementById('user-name').value;
    const email = document.getElementById('user-email').value;
    const bio = document.getElementById('user-bio').value;
    const avatar = document.getElementById('user-avatar').value;

    try {
        await APIClient.createUser(name, email, bio, avatar);
        showToast('Benutzer erfolgreich erstellt!', 'success');
        closeUserModal();
        loadUsers();
    } catch (error) {
        console.error('Error creating user:', error);
        showToast('Fehler beim Erstellen des Benutzers', 'error');
    }
}

async function deleteUser(userId) {
    if (!confirm('Möchten Sie diesen Benutzer wirklich löschen?')) {
        return;
    }

    try {
        await APIClient.deleteUser(userId);
        showToast('Benutzer erfolgreich gelöscht!', 'success');
        loadUsers();
    } catch (error) {
        console.error('Error deleting user:', error);
        showToast('Fehler beim Löschen des Benutzers', 'error');
    }
}

function filterUsers() {
    const searchTerm = document.getElementById('user-search').value.toLowerCase();
    const rows = document.querySelectorAll('#users-list tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// ========== PRODUCTS ==========

async function loadProducts() {
    try {
        const response = await APIClient.getProducts();
        const products = response.data || [];

        const productsList = document.getElementById('products-list');
        
        if (products.length === 0) {
            productsList.innerHTML = '<div class="loading">Keine Produkte gefunden</div>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Preis (€)</th>
                        <th>Besitzer ID</th>
                        <th>Beschreibung</th>
                        <th>Aktionen</th>
                    </tr>
                </thead>
                <tbody>
        `;

        products.forEach(product => {
            html += `
                <tr>
                    <td>${product.id}</td>
                    <td>${product.name || '-'}</td>
                    <td>${(product.price || 0).toFixed(2)}</td>
                    <td>${product.ownerId || '-'}</td>
                    <td>${product.description || '-'}</td>
                    <td>
                        <button class="btn btn-danger btn-small" onclick="deleteProduct(${product.id})">
                            <i class="fas fa-trash"></i> Löschen
                        </button>
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        productsList.innerHTML = html;
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('Fehler beim Laden der Produkte', 'error');
    }
}

function showProductModal() {
    document.getElementById('product-modal').classList.add('show');
}

function closeProductModal() {
    document.getElementById('product-modal').classList.remove('show');
    document.getElementById('product-form').reset();
}

async function submitProductForm(event) {
    event.preventDefault();

    const name = document.getElementById('product-name').value;
    const price = parseFloat(document.getElementById('product-price').value);
    const owner = parseInt(document.getElementById('product-owner').value);
    const description = document.getElementById('product-description').value;

    try {
        await APIClient.createProduct(name, price, owner, description);
        showToast('Produkt erfolgreich erstellt!', 'success');
        closeProductModal();
        loadProducts();
    } catch (error) {
        console.error('Error creating product:', error);
        showToast('Fehler beim Erstellen des Produkts', 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('Möchten Sie dieses Produkt wirklich löschen?')) {
        return;
    }

    try {
        await APIClient.deleteProduct(productId);
        showToast('Produkt erfolgreich gelöscht!', 'success');
        loadProducts();
    } catch (error) {
        console.error('Error deleting product:', error);
        showToast('Fehler beim Löschen des Produkts', 'error');
    }
}

function filterProducts() {
    const searchTerm = document.getElementById('product-search').value.toLowerCase();
    const rows = document.querySelectorAll('#products-list tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// ========== ORDERS ==========

async function loadOrders() {
    try {
        const response = await APIClient.getOrders();
        const orders = response.data || [];

        const ordersList = document.getElementById('orders-list');
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<div class="loading">Keine Bestellungen gefunden</div>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Benutzer ID</th>
                        <th>Produkt ID</th>
                        <th>Menge</th>
                        <th>Gesamtpreis (€)</th>
                        <th>Status</th>
                        <th>Aktionen</th>
                    </tr>
                </thead>
                <tbody>
        `;

        orders.forEach(order => {
            html += `
                <tr>
                    <td>${order.id}</td>
                    <td>${order.userId || '-'}</td>
                    <td>${order.productId || '-'}</td>
                    <td>${order.quantity || 0}</td>
                    <td>${(order.totalPrice || 0).toFixed(2)}</td>
                    <td><span class="badge">${order.status || 'pending'}</span></td>
                    <td>
                        <button class="btn btn-danger btn-small" onclick="deleteOrder(${order.id})">
                            <i class="fas fa-trash"></i> Löschen
                        </button>
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        ordersList.innerHTML = html;
    } catch (error) {
        console.error('Error loading orders:', error);
        showToast('Fehler beim Laden der Bestellungen', 'error');
    }
}

function showOrderModal() {
    document.getElementById('order-modal').classList.add('show');
}

function closeOrderModal() {
    document.getElementById('order-modal').classList.remove('show');
    document.getElementById('order-form').reset();
}

async function submitOrderForm(event) {
    event.preventDefault();

    const userId = parseInt(document.getElementById('order-user').value);
    const productId = parseInt(document.getElementById('order-product').value);
    const quantity = parseInt(document.getElementById('order-quantity').value);
    const totalPrice = parseFloat(document.getElementById('order-price').value);

    try {
        await APIClient.createOrder(userId, productId, quantity, totalPrice);
        showToast('Bestellung erfolgreich erstellt!', 'success');
        closeOrderModal();
        loadOrders();
    } catch (error) {
        console.error('Error creating order:', error);
        showToast('Fehler beim Erstellen der Bestellung', 'error');
    }
}

async function deleteOrder(orderId) {
    if (!confirm('Möchten Sie diese Bestellung wirklich löschen?')) {
        return;
    }

    try {
        await APIClient.deleteOrder(orderId);
        showToast('Bestellung erfolgreich gelöscht!', 'success');
        loadOrders();
    } catch (error) {
        console.error('Error deleting order:', error);
        showToast('Fehler beim Löschen der Bestellung', 'error');
    }
}

function filterOrders() {
    const searchTerm = document.getElementById('order-search').value.toLowerCase();
    const rows = document.querySelectorAll('#orders-list tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// ========== UTILITIES ==========

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// auth.js - Shared authentication logic
const Auth = {
    login: async (username, password) => {
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (data.status === 'success') {
                localStorage.setItem('qkd_user', JSON.stringify(data));
                return { success: true };
            }
            return { success: false, message: data.message };
        } catch (error) {
            return { success: false, message: 'Server connection failed' };
        }
    },

    logout: () => {
        localStorage.removeItem('qkd_user');
        window.location.href = '/';
    },

    getUser: () => {
        const user = localStorage.getItem('qkd_user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('qkd_user');
    },

    isAdmin: () => {
        const user = Auth.getUser();
        return user && user.role === 'admin';
    },

    checkAccess: (requiredRole = null) => {
        const user = Auth.getUser();
        if (!user) {
            window.location.href = '/login.html';
            return false;
        }
        if (requiredRole && user.role !== requiredRole) {
            window.location.href = '/app.html'; // Default redirect
            return false;
        }
        return true;
    },

    updateNavbar: () => {
        const user = Auth.getUser();
        const navLinks = document.querySelector('.nav-links');
        if (!navLinks) return;

        if (user) {
            // Logged In
            let links = `
                <a href="/app.html">Simulator</a>
                ${user.role === 'admin' ? '<a href="/admin.html">Admin Panel</a>' : ''}
                <a href="#" id="logout-btn" class="btn btn-secondary">Sign Out</a>
            `;
            navLinks.innerHTML = links;
            document.getElementById('logout-btn').addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        } else {
            // Logged Out
            navLinks.innerHTML = `
                <a href="#features">Features</a>
                <a href="/login.html" class="btn btn-primary">Sign In</a>
            `;
        }
    }
};

// Initialize navbar on load if not on login page
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.nav-links')) {
        Auth.updateNavbar();
    }
});

/**
 * Authentication API client
 * Handles user registration, login, token refresh, and logout
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Register a new user
 * @param {string} email - User email
 * @param {string} fullName - User full name
 * @param {string} password - User password (min 8 characters)
 * @returns {Promise<{id, email, full_name, role, is_active, created_at, updated_at}>}
 */
export const registerUser = async (email, fullName, password) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      full_name: fullName,
      password,
      role: 'researcher'
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }

  return await response.json();
};

/**
 * Login user with email and password
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<{access_token, refresh_token, token_type}>}
 */
export const loginUser = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  const data = await response.json();
  
  // Store tokens in localStorage
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('token_type', data.token_type);
  
  return data;
};

/**
 * Request a password reset link to be emailed to the user
 * @param {string} email - User email
 * @returns {Promise<{detail: string}>}
 */
export const requestPasswordReset = async (email) => {
  const response = await fetch(`${API_URL}/auth/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Could not send reset email');
  }

  return await response.json();
};

/**
 * Get current user information
 * @param {string} accessToken - JWT access token
 * @returns {Promise<{id, email, full_name, role, is_active, created_at, updated_at}>}
 */
export const getCurrentUser = async (accessToken) => {
  const response = await fetch(`${API_URL}/auth/me`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user info');
  }

  return await response.json();
};

/**
 * Refresh access token using refresh token
 * @param {string} refreshToken - JWT refresh token
 * @returns {Promise<{access_token, refresh_token, token_type}>}
 */
export const refreshAccessToken = async (refreshToken) => {
  const response = await fetch(`${API_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
  });

  if (!response.ok) {
    throw new Error('Token refresh failed');
  }

  const data = await response.json();
  
  // Update tokens in localStorage
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data;
};

/**
 * Logout user (clear tokens)
 */
export const logoutUser = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('token_type');
  localStorage.removeItem('user');
};

/**
 * Get stored access token
 * @returns {string|null}
 */
export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

/**
 * Get stored refresh token
 * @returns {string|null}
 */
export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

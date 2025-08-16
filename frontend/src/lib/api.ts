import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.warn('Failed to access localStorage:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      console.error('Network Error: Backend server is not running');
      error.message = 'Network Error: Please ensure the backend server is running at ' + API_BASE_URL;
    }
    
    if (error.response?.status === 401) {
      // Token expired or invalid
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// API helper functions
export const api = {
  // Health check
  health: () => apiClient.get('/health'),
  
  // Products
  getProducts: (params?: { search?: string; rating?: string; limit?: number; skip?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.rating) searchParams.append('rating', params.rating);
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    
    return apiClient.get(`/api/v1/products/?${searchParams.toString()}`);
  },
  
  getProduct: (id: number) => apiClient.get(`/api/v1/products/${id}`),
  
  // Reviews
  getProductReviews: (productId: number) => apiClient.get(`/api/v1/reviews/product/${productId}`),
  
  // Auth
  login: (email: string, password: string) => 
    apiClient.post('/api/v1/auth/login', { email, password }),
  
  register: (userData: { first_name: string; last_name: string; email: string; password: string }) =>
    apiClient.post('/api/v1/auth/register', userData),
  
  getCurrentUser: () => apiClient.get('/api/v1/auth/me'),
};

export default apiClient;
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';

interface User {
  customer_id: number;
  first_name: string;
  last_name: string;
  email: string;
  is_admin: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        fetchUser();
      } else {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await apiClient.get('/auth/me');
      setUser(response.data);
    } catch (error) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    // Sanitize inputs to prevent XSS
    const sanitizedEmail = email.trim().toLowerCase();
    const response = await apiClient.post('/auth/login', { 
      email: sanitizedEmail, 
      password 
    });
    const { access_token, user: userData } = response.data;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', access_token);
    }
    // Sanitize user data before setting
    const sanitizedUser = {
      ...userData,
      first_name: userData.first_name?.replace(/[<>"'&]/g, ''),
      last_name: userData.last_name?.replace(/[<>"'&]/g, ''),
      email: userData.email?.replace(/[<>"'&]/g, '')
    };
    setUser(sanitizedUser);
  };

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
import axios from 'axios';
import { User } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

interface TokenRefreshResponse {
  access: string;
}

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
};

const authService = {
  register: async (username: string, email: string, password: string, password_confirm: string, first_name: string = '', last_name: string = ''): Promise<User> => {
    const response = await axios.post<User>(
      `${API_BASE_URL}/users/register/`, 
      {
        username,
        email,
        password,
        password_confirm,
        first_name,
        last_name
      },
      { headers: { 'Content-Type': 'application/json' } }
    );
    return response.data;
  },

  login: async (username: string, password: string): Promise<User> => {
    const response = await axios.post<AuthResponse>(
      `${API_BASE_URL}/users/login/`, 
      { username, password },
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('refreshToken', response.data.refresh);
    
    const userProfile = await axios.get<User>(
      `${API_BASE_URL}/users/profile/`,
      { headers: getAuthHeaders() }
    );
    return userProfile.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },

  getProfile: async (): Promise<User> => {
    const response = await axios.get<User>(
      `${API_BASE_URL}/users/profile/`,
      { headers: getAuthHeaders() }
    );
    return response.data;
  },

  refreshToken: async (): Promise<string> => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await axios.post<TokenRefreshResponse>(
      `${API_BASE_URL}/users/token/refresh/`, 
      { refresh: refreshToken },
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    localStorage.setItem('token', response.data.access);
    return response.data.access;
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  }
};

export default authService;

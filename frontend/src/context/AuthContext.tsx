import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState, User } from '../types';
import { authService } from '../services';

type AuthAction =
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'REGISTER_SUCCESS'; payload: User }
  | { type: 'REGISTER_FAILURE'; payload: string }
  | { type: 'CLEAR_ERROR' };

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null
};

const AuthContext = createContext<{
  state: AuthState;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, password_confirm: string, first_name?: string, last_name?: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}>({
  state: initialState,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  clearError: () => {}
});

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
    case 'REGISTER_SUCCESS':
      localStorage.setItem('user', JSON.stringify(action.payload));
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        loading: false,
        error: null
      };
    case 'LOGIN_FAILURE':
    case 'REGISTER_FAILURE':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: action.payload
      };
    case 'LOGOUT':
      localStorage.removeItem('user');
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    const fetchUserProfile = async () => {
      if (authService.isAuthenticated()) {
        try {
          const user = await authService.getProfile();
          dispatch({ type: 'LOGIN_SUCCESS', payload: user });
        } catch (error) {
          authService.logout();
        }
      }
    };
    
    fetchUserProfile();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const user = await authService.login(username, password);
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Invalid credentials' });
    }
  };

  const register = async (username: string, email: string, password: string, password_confirm: string, first_name?: string, last_name?: string) => {
    try {
      const user = await authService.register(username, email, password, password_confirm, first_name || '', last_name || '');
      dispatch({ type: 'REGISTER_SUCCESS', payload: user });
    } catch (error: any) {
      let errorMessage = 'Registration failed';
      if (error.response && error.response.data) {
        errorMessage = error.response.data.detail || JSON.stringify(error.response.data);
      }
      dispatch({ type: 'REGISTER_FAILURE', payload: errorMessage });
    }
  };

  const logout = () => {
    authService.logout();
    dispatch({ type: 'LOGOUT' });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  return (
    <AuthContext.Provider value={{ state, login, register, logout, clearError }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

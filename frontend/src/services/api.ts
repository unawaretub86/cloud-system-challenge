import axios, { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

interface RefreshTokenResponse {
  access: string;
  refresh?: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';


const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});


api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);


let isRefreshing = false;

let refreshSubscribers: ((token: string) => void)[] = [];


const subscribeToTokenRefresh = (callback: (token: string) => void): void => {
  refreshSubscribers.push(callback);
};


const onTokenRefreshed = (newToken: string): void => {
  refreshSubscribers.forEach(callback => callback(newToken));
  refreshSubscribers = [];
};


api.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => response,
  async (error: AxiosError): Promise<any> => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (
      error.response?.status === 401 && 
      !originalRequest._retry && 
      originalRequest.url !== '/users/token/refresh/' &&
      originalRequest.url !== '/users/login/'
    ) {
      if (!isRefreshing) {
        isRefreshing = true;
        originalRequest._retry = true;
        
        try {
          const refreshToken = localStorage.getItem('refreshToken');
          if (!refreshToken) {
            throw new Error('No refresh token available');
          }
          

          const refreshResponse = await axios.post<RefreshTokenResponse>(
            `${API_BASE_URL}/users/token/refresh/`,
            { refresh: refreshToken },
            { headers: { 'Content-Type': 'application/json' } }
          );
          
          const { access: newAccessToken, refresh: newRefreshToken } = refreshResponse.data;
          

          localStorage.setItem('token', newAccessToken);
          if (newRefreshToken) {
            localStorage.setItem('refreshToken', newRefreshToken);
          }
          

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          

          onTokenRefreshed(newAccessToken);
          isRefreshing = false;

          return axios(originalRequest);
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);

          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          isRefreshing = false;
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {

        return new Promise(resolve => {
          subscribeToTokenRefresh(newToken => {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            resolve(axios(originalRequest));
          });
        });
      }
    }
    

    const errorResponse = {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message || 'Unknown error occurred'
    };
    
    console.error('API Error:', errorResponse);
    return Promise.reject(errorResponse);
  }
);

export default api;

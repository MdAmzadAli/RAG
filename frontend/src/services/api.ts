import axios from 'axios';
import type { AxiosInstance } from 'axios';
const API: AxiosInstance = axios.create({ baseURL: 'http://localhost:8000' });

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;

import axios from "axios";
import { useAuthStore } from "@/stores/auth.store";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// axios instance configurada con interceptores
export const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
});

// request interceptor: agregar token a headers
apiClient.interceptors.request.use(
  (config) => {
    const tokens = useAuthStore.getState().tokens;
    if (tokens?.access_token) {
      config.headers.Authorization = `Bearer ${tokens.access_token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// response interceptor: manejar refresh token en 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Intentar refrescar el token
        await useAuthStore.getState().refreshToken();
        // Reintentar request original con nuevo token
        const tokens = useAuthStore.getState().tokens;
        originalRequest.headers.Authorization = `Bearer ${tokens?.access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Si falla el refresh, redirigir a login
        useAuthStore.getState().logout();
        if (typeof window !== "undefined") {
          window.location.href = "/";
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

import { apiClient } from "./client";
import type {
  LoginCredentials,
  RegisterData,
  AuthResponse,
  AuthTokens,
} from "@/types/auth.types";

// api endpoints para autenticacion

export async function loginUser(
  credentials: LoginCredentials
): Promise<AuthResponse> {
  // 1. Login y obtener tokens
  // OAuth2 requiere form-data con campo 'username' (no 'email')
  const formData = new URLSearchParams();
  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const tokenResponse = await apiClient.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  const tokens: AuthTokens = tokenResponse.data;

  // 2. Obtener datos del usuario con el token
  const userResponse = await apiClient.get("/auth/me", {
    headers: {
      Authorization: `Bearer ${tokens.access_token}`,
    },
  });

  return {
    user: userResponse.data,
    tokens,
  };
}

export async function registerUser(data: RegisterData): Promise<AuthResponse> {
  // 1. Registrar y obtener tokens
  const tokenResponse = await apiClient.post("/auth/register", data);
  const tokens: AuthTokens = tokenResponse.data;

  // 2. Obtener datos del usuario con el token
  const userResponse = await apiClient.get("/auth/me", {
    headers: {
      Authorization: `Bearer ${tokens.access_token}`,
    },
  });

  return {
    user: userResponse.data,
    tokens,
  };
}

export async function refreshAccessToken(
  refreshToken: string
): Promise<AuthTokens> {
  const response = await apiClient.post("/auth/refresh", {
    refresh_token: refreshToken,
  });
  return response.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get("/auth/me");
  return response.data;
}

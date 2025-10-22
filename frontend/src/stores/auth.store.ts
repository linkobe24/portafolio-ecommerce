import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type {
  AuthStore,
  LoginCredentials,
  RegisterData,
} from "@/types/auth.types";
import {
  loginUser,
  registerUser,
  refreshAccessToken,
} from "@/lib/api/auth.api";
import axios from "axios";

// zustand store para manejo de autenticacion
// usa persist middleware para mantener sesion en localStorage

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      //login action
      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true, error: null });
        try {
          const response = await loginUser(credentials);
          set({
            user: response.user,
            tokens: response.tokens,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: unknown) {
          if (axios.isAxiosError(error)) {
            set({
              error: error.response?.data?.message || "Error al iniciar sesión",
              isLoading: false,
            });
          } else {
            set({
              error: "Error desconocido",
              isLoading: false,
            });
          }
          throw error;
        }
      },

      //register action
      register: async (data: RegisterData) => {
        set({ isLoading: true, error: null });
        try {
          const response = await registerUser(data);
          set({
            user: response.user,
            tokens: response.tokens,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: unknown) {
          if (axios.isAxiosError(error)) {
            set({
              error: error.response?.data?.message || "Error al registrarse",
              isLoading: false,
            });
          } else {
            set({
              error: "Error desconocido",
              isLoading: false,
            });
          }
          throw error;
        }
      },

      //logout action
      logout: () => {
        set({
          user: null,
          tokens: null,
          isAuthenticated: false,
          error: null,
        });
      },

      //refresh token action
      refreshToken: async () => {
        const { tokens } = get();
        if (!tokens?.refresh_token) {
          throw new Error("No refresh token available");
        }
        try {
          const newTokens = await refreshAccessToken(tokens.refresh_token);
          set({ tokens: newTokens });
        } catch (error) {
          // si falla refresh hacer logout
          get().logout();
          throw error;
        }
      },

      // setters auxiliares
      setUser: (user) => set({ user }),
      setTokens: (tokens) => set({ tokens }),
      setError: (error) => set({ error }),
      clearError: () => set({ error: null }),
    }),
    {
      name: "auth-storage", // key in localStorage
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

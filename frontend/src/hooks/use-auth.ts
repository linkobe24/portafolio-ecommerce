import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "next/navigation";
import { useCallback } from "react";
import type { LoginCredentials, RegisterData } from "@/types/auth.types";

// facilita el uso de auth store en componentes

export function useAuth() {
  const router = useRouter();
  const store = useAuthStore();

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      await store.login(credentials);
      router.push("/"); // redirigir a home despues del login
    },
    [store, router]
  );

  const register = useCallback(
    async (data: RegisterData) => {
      await store.register(data);
      router.push("/");
    },
    [store, router]
  );

  const logout = useCallback(() => {
    store.logout();
    router.push("/");
  }, [store, router]);

  return {
    // estado
    user: store.user,
    isAuthenticated: store.isAuthenticated,
    isLoading: store.isLoading,
    error: store.error,

    //actions
    login,
    register,
    logout,
    clearError: store.clearError,
  };
}

// redirige a home si el usuario no esta autenticado o no tiene permisos.

"use client";

import { useAuth } from "@/hooks/use-auth";
import { useRouter } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

type AuthGuardProps = {
  children: ReactNode;
  requireAdmin?: boolean;
};

export function AuthGuard({ children, requireAdmin = false }: AuthGuardProps) {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  // Esperar a que el componente esté montado (hidratación de Zustand)
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return; // Esperar a que se monte

    if (!isAuthenticated) {
      router.push("/");
      return;
    }

    if (requireAdmin && user?.role !== "admin") {
      router.push("/");
    }
  }, [mounted, isAuthenticated, user, requireAdmin, router]);

  // Mostrar loading mientras se monta o verifica auth
  if (!mounted || !isAuthenticated || (requireAdmin && user?.role !== "admin")) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return <>{children}</>;
}

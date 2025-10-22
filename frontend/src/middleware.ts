import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// middleware de nextjs para proteger rutas privadas.

export function middleware(request: NextRequest) {
  // rutas que requieren autenticación
  const protectedPaths = ["/profile", "/orders", "/checkout"];
  const adminPaths = ["/admin"];

  const { pathname } = request.nextUrl;

  // verificar si es ruta protegida
  const isProtectedPath = protectedPaths.some((path) =>
    pathname.startsWith(path)
  );
  const isAdminPath = adminPaths.some((path) => pathname.startsWith(path));

  const authStorage = request.cookies.get("auth-storage"); // zustan guarda en localStorage pero es el patron

  if (isProtectedPath || isAdminPath) {
    if (!authStorage) {
      return NextResponse.redirect(new URL("/", request.url));
    }

    // Si es ruta admin, verificar role
    if (isAdminPath) {
      try {
        const auth = JSON.parse(authStorage.value);
        if (auth.state?.user?.role !== "admin") {
          return NextResponse.redirect(new URL("/", request.url));
        }
      } catch {
        return NextResponse.redirect(new URL("/", request.url));
      }
    }
  }

  return NextResponse.next();
}

// Matcher vacío = middleware deshabilitado
// Protección de rutas se maneja con AuthGuard (client-side) en cada página
export const config = {
  matcher: [],
};

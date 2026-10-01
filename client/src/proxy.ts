import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "./lib/auth";
import { headers } from "next/headers";

/**
 * Proxy Middleware de Autenticación
 *
 * Reglas de navegación:
 * 1. Rutas de solo invitados (página principal "/" y rutas de autenticación "/auth/*"):
 *    - Si el usuario TIENE sesión activa -> Redirige a "/home".
 * 2. Rutas protegidas ("/home/*"):
 *    - Si el usuario NO tiene sesión activa -> Redirige a "/auth/login".
 */
export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Obtener la sesión activa de Better Auth
  let session = null;
  try {
    session = await auth.api.getSession({
      headers: await headers(),
    });
  } catch {
    try {
      session = await auth.api.getSession({
        headers: request.headers,
      });
    } catch {
      session = null;
    }
  }

  const isAuthenticated = !!session;

  const isGuestOnlyRoute = pathname === "/" || pathname.startsWith("/auth");
  const isProtectedRoute = pathname.startsWith("/home");

  // 1. Si está autenticado e intenta acceder a la landing ("/") o rutas de autenticación -> Redirigir a /home
  if (isAuthenticated && isGuestOnlyRoute) {
    return NextResponse.redirect(new URL("/home", request.url));
  }

  // 2. Si NO está autenticado e intenta acceder a rutas protegidas -> Redirigir a /auth/login
  if (!isAuthenticated && isProtectedRoute) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/auth/:path*", "/home/:path*"],
};


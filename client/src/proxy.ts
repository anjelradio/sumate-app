import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "./lib/auth";
import { headers } from "next/headers";

/**
 * Proxy Middleware de Autenticación
 *
 * Reglas de navegación:
 * 1. Rutas de solo invitados (página principal "/" y rutas de autenticación "/auth/*"):
 *    - Si el usuario TIENE sesión activa -> Redirige a "/explore".
 * 2. Trampolín de compatibilidad ("/home"):
 *    - Si el usuario TIENE sesión activa -> Redirige a "/explore".
 *    - Si el usuario NO tiene sesión activa -> Redirige a "/auth/login".
 * 3. Rutas protegidas ("/explore", "/my-activities", "/recently"):
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
  const isHomeTrampoline = pathname === "/home" || pathname.startsWith("/home/");
  const isProtectedRoute =
    isHomeTrampoline ||
    pathname.startsWith("/explore") ||
    pathname.startsWith("/my-activities") ||
    pathname.startsWith("/recently");

  if (isAuthenticated && isGuestOnlyRoute) {
    return NextResponse.redirect(new URL("/explore", request.url));
  }

  if (isAuthenticated && isHomeTrampoline) {
    return NextResponse.redirect(new URL("/explore", request.url));
  }

  if (!isAuthenticated && isProtectedRoute) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/auth/:path*",
    "/home",
    "/home/:path*",
    "/explore",
    "/explore/:path*",
    "/my-activities",
    "/my-activities/:path*",
    "/recently",
    "/recently/:path*",
  ],
};


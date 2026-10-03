/**
 * Service Worker para Súmate PWA
 * Gestiona instalación, activación y soporte offline básico.
 */

const CACHE_NAME = "sumate-pwa-v2";
const OFFLINE_URL = "/offline.html";

const PRECACHE_ASSETS = [
  "/",
  OFFLINE_URL,
  "/icons/icon-192x192.png",
  "/icons/icon-512x512.png",
  "/icons/icon-maskable-192x192.png",
  "/icons/icon-maskable-512x512.png",
  "/icons/apple-touch-icon.png",
  "/apple-touch-icon.png",
  "/favicon.ico"
];

// Instalación: precarga recursos esenciales
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activación: limpia caches obsoletos y toma control de clientes
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName !== CACHE_NAME)
          .map((cacheName) => caches.delete(cacheName))
      );
    })
  );
  self.clients.claim();
});

// Fetch: estrategia de red primero con fallback a cache o página offline
self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Solo interceptamos peticiones GET
  if (request.method !== "GET") return;

  // Si es una navegación HTML (usuario cambiando de página)
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(async () => {
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(request);
        if (cachedResponse) return cachedResponse;
        return cache.match(OFFLINE_URL);
      })
    );
    return;
  }

  // Para recursos estáticos (imágenes de iconos, estilos, scripts)
  if (
    request.destination === "image" ||
    request.destination === "style" ||
    request.destination === "script" ||
    request.destination === "font"
  ) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) return cachedResponse;

        return fetch(request)
          .then((networkResponse) => {
            if (
              networkResponse &&
              networkResponse.status === 200 &&
              networkResponse.type === "basic"
            ) {
              const responseToCache = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseToCache);
              });
            }
            return networkResponse;
          })
          .catch(() => {
            // Si falla la red y es imagen, no hacemos nada o devolvemos placeholder
            return cachedResponse;
          });
      })
    );
  }
});

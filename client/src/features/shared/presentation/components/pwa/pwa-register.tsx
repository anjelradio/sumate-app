"use client";

import { useEffect } from "react";

export function PwaRegister() {
  useEffect(() => {
    if (typeof window !== "undefined" && "serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker
          .register("/sw.js")
          .then((registration) => {
            // Service worker registrado
            registration.update();
          })
          .catch((error) => {
            console.error("[PWA] Error al registrar el Service Worker:", error);
          });
      });
    }
  }, []);

  return null;
}

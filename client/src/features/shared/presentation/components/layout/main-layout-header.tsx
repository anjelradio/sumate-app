"use client";

import { usePathname } from "next/navigation";
import { AppHeader } from "./app-header";
import { AppNavbar } from "./app-navbar";

export function MainLayoutHeader() {
  const pathname = usePathname();

  if (pathname === "/search") {
    return null;
  }

  return (
    <header className="shrink-0 z-40 bg-white">
      <AppHeader />
      <AppNavbar />
    </header>
  );
}

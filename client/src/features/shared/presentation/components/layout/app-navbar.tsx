"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { NAVIGATION_ITEMS } from "../../config/navigation.config";

export function AppNavbar() {
  const pathname = usePathname();

  return (
    <nav
      aria-label="Pestañas de navegación principal"
      className="flex items-center overflow-x-auto no-scrollbar bg-white"
      role="tablist"
    >
      {NAVIGATION_ITEMS.filter((item) => item.enabled).map((item) => {
        const isActive =
          pathname === item.href ||
          (item.href !== "/" && pathname.startsWith(`${item.href}/`));

        return (
          <Link
            key={item.id}
            href={item.href}
            role="tab"
            prefetch={true}
            aria-selected={isActive}
            className={`flex-1 flex flex-col items-center justify-center pt-2.5 pb-2 transition-all shrink-0 min-w-[70px] border-b-2 ${
              isActive
                ? "border-black text-black font-bold"
                : "border-transparent text-zinc-600 font-medium hover:text-black"
            }`}
          >
            <div className="relative w-[26px] h-[26px] mb-1 shrink-0">
              <Image
                src={item.iconUrl}
                alt=""
                fill
                sizes="26px"
                className="object-contain"
              />
            </div>
            <span className="text-xs tracking-tight">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

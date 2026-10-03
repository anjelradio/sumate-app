"use client";

import Link from "next/link";
import { Compass, CalendarCheck } from "lucide-react";
import type { EventScope } from "@/features/events/domain/entities/event.entity";
import { cn } from "@/lib/utils";

type EventsSegmentedNavProps = {
  activeScope: EventScope;
};

export function EventsSegmentedNav({ activeScope }: EventsSegmentedNavProps) {
  const isMine = activeScope === "mine";
  const isOthers = activeScope === "others";

  return (
    <nav aria-label="Selector de pestañas de eventos" className="mt-3 mb-2" data-purpose="segmented-tabs">
      <div className="grid grid-cols-2 p-1.5 bg-[#f1f3ff] rounded-full border border-[#ece9fc]/80 shadow-sm" role="tablist">
        {/* Pestaña: Mis eventos (Por defecto) */}
        <Link
          href="/home?scope=mine"
          replace
          role="tab"
          aria-selected={isMine}
          className={cn(
            "flex items-center justify-center gap-2 py-2 px-3 text-sm font-semibold rounded-full transition-all focus:outline-none cursor-pointer",
            isMine
              ? "bg-[#6355de] text-white shadow-md shadow-[#6355de]/25"
              : "text-zinc-600 hover:text-zinc-900"
          )}
        >
          <CalendarCheck className={cn("w-4 h-4 shrink-0", isMine ? "text-white" : "text-zinc-500")} />
          <span>Mis eventos</span>
        </Link>

        {/* Pestaña: Explorar eventos (Eventos de otros) */}
        <Link
          href="/home?scope=others"
          replace
          role="tab"
          aria-selected={isOthers}
          className={cn(
            "flex items-center justify-center gap-2 py-2 px-3 text-sm font-semibold rounded-full transition-all focus:outline-none cursor-pointer",
            isOthers
              ? "bg-[#6355de] text-white shadow-md shadow-[#6355de]/25"
              : "text-zinc-600 hover:text-zinc-900"
          )}
        >
          <Compass className={cn("w-4 h-4 shrink-0", isOthers ? "text-white" : "text-zinc-500")} />
          <span>Explorar eventos</span>
        </Link>
      </div>
    </nav>
  );
}

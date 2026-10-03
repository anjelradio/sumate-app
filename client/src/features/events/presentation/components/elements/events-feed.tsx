import { CalendarX } from "lucide-react";
import type { EventListItem, EventScope } from "@/features/events/domain/entities/event.entity";
import { EventCard } from "./event-card";

type EventsFeedProps = {
  events: EventListItem[];
  scope: EventScope;
};

export function EventsFeed({ events, scope }: EventsFeedProps) {
  if (events.length === 0) {
    const isMine = scope === "mine";
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
        <div className="w-16 h-16 rounded-full bg-[#f1f3ff] text-[#6355de] flex items-center justify-center mb-3 shadow-inner">
          <CalendarX className="w-8 h-8" />
        </div>
        <h3 className="text-lg font-bold text-zinc-800">
          {isMine ? "Aún no has creado eventos" : "No hay eventos comunitarios"}
        </h3>
        <p className="text-sm text-zinc-500 mt-1 max-w-xs leading-relaxed">
          {isMine
            ? "Toca el botón '+ Crear evento' para publicar tu primera iniciativa solidaria."
            : "Actualmente no hay convocatorias de otros miembros disponibles."}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4 pt-1" data-purpose="events-feed">
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}

import Image from "next/image";
import { Calendar } from "lucide-react";
import type { EventListItem } from "@/features/events/domain/entities/event.entity";

type EventCardProps = {
  event: EventListItem;
};

function formatEventDate(dateString: string): string {
  try {
    const d = new Date(dateString);
    if (isNaN(d.getTime())) return dateString;

    const formatted = d.toLocaleDateString("es-ES", {
      weekday: "short",
      day: "numeric",
      month: "short",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });

    // Capitalizar primera letra (ej. "Sáb, 15 oct • 8:30 AM")
    return formatted.charAt(0).toUpperCase() + formatted.slice(1);
  } catch {
    return dateString;
  }
}

export function EventCard({ event }: EventCardProps) {
  const formattedDate = formatEventDate(event.date);

  return (
    <article
      className="bg-white rounded-3xl p-3.5 shadow-sm border border-zinc-100 transition-transform active:scale-[0.99] text-left"
      data-purpose="event-card"
    >
      {/* Imagen del evento */}
      <div className="relative w-full h-44 rounded-2xl overflow-hidden bg-zinc-100">
        <Image
          src={event.imageUrl}
          alt={event.name}
          fill
          unoptimized
          sizes="(max-width: 768px) 100vw, 450px"
          className="object-cover"
        />
      </div>

      {/* Información del evento */}
      <div className="pt-3 px-1 pb-1">
        <h2 className="text-base font-bold text-zinc-900 leading-snug line-clamp-2">
          {event.name}
        </h2>

        <p className="mt-1.5 text-xs font-semibold text-[#6355de] flex items-center">
          <Calendar className="w-3.5 h-3.5 mr-1.5 text-[#6355de] shrink-0" />
          <span>{formattedDate}</span>
        </p>

        {event.creatorName && (
          <p className="mt-1 text-xs text-zinc-500">
            Por <span className="font-semibold text-zinc-700">{event.creatorName}</span>
          </p>
        )}
      </div>
    </article>
  );
}

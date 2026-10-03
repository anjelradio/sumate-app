import Image from "next/image";
import type { ActivityListItem } from "@/features/activities/domain/entities/activity.entity";

type ActivityCardProps = {
  activity: ActivityListItem;
};

function formatActivityDate(dateString: string): string {
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

export function ActivityCard({ activity }: ActivityCardProps) {
  const formattedDate = formatActivityDate(activity.date);

  return (
    <article
      className="pb-6 mb-6 border-b border-slate-100 transition-transform active:scale-[0.99] text-left last:border-b-0 last:mb-0 last:pb-0"
      data-purpose="activity-card"
    >
      {/* Imagen de la actividad con esquinas redondeadas */}
      <div className="relative w-full h-44 rounded-2xl overflow-hidden bg-slate-100">
        <Image
          src={activity.imageUrl}
          alt={activity.name}
          fill
          unoptimized
          sizes="(max-width: 768px) 100vw, 450px"
          className="object-cover"
        />
      </div>

      {/* Información de la actividad */}
      <div className="pt-3 px-1">
        <h2 className="text-base font-bold text-slate-900 leading-snug line-clamp-2">
          {activity.name}
        </h2>

        <p className="mt-1.5 text-xs font-semibold text-zinc-700 flex items-center gap-1.5">
          <div className="relative w-3.5 h-3.5 shrink-0">
            <Image
              src="/assets/icons/date.webp"
              alt=""
              fill
              sizes="14px"
              className="object-contain"
            />
          </div>
          <span>{formattedDate}</span>
        </p>

        {activity.creatorName && (
          <p className="mt-1 text-xs text-slate-500">
            Por <span className="font-semibold text-slate-700">{activity.creatorName}</span>
          </p>
        )}
      </div>
    </article>
  );
}

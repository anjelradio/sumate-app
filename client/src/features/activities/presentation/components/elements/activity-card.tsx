import Image from "next/image";
import { Calendar, Users } from "lucide-react";
import type { ActivityListItem, ActivityScope } from "@/features/activities/domain/entities/activity.entity";

type ActivityCardProps = {
  activity: ActivityListItem;
  scope?: ActivityScope;
};

function formatActivityDate(dateString: string): string {
  try {
    // Si no contiene indicador de timezone ('Z' o '+' o '-'), asegurar UTC para evitar desfases
    const isoString =
      dateString.includes("Z") || dateString.includes("+") || dateString.includes("-", 10)
        ? dateString
        : `${dateString}Z`;

    const d = new Date(isoString);
    if (isNaN(d.getTime())) return dateString;

    // Obtener componentes por separado en hora boliviana (La Paz, UTC-4)
    const weekday = d.toLocaleDateString("es-BO", { timeZone: "America/La_Paz", weekday: "short" });
    const day = d.toLocaleDateString("es-BO", { timeZone: "America/La_Paz", day: "numeric" });
    const month = d.toLocaleDateString("es-BO", { timeZone: "America/La_Paz", month: "short" });
    const time = d.toLocaleTimeString("es-BO", {
      timeZone: "America/La_Paz",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });

    const capWeekday = weekday.charAt(0).toUpperCase() + weekday.slice(1);
    return `${capWeekday}, ${day} ${month} • ${time}`;
  } catch {
    return dateString;
  }
}

export function ActivityCard({ activity, scope }: ActivityCardProps) {
  const formattedDate = formatActivityDate(activity.date);

  const getStatusBadge = () => {
    switch (activity.status) {
      case "draft":
        return {
          label: "Borrador",
          className: "bg-amber-50 text-amber-700 border border-amber-200/70",
        };
      case "active":
        return {
          label: "Activa",
          className: "bg-emerald-50 text-emerald-700 border border-emerald-200/70",
        };
      case "closed":
        return {
          label: "Cerrada",
          className: "bg-slate-100 text-slate-600 border border-slate-200/70",
        };
      default:
        return null;
    }
  };

  const statusBadge = getStatusBadge();
  const showStatusBadge = scope === "mine" || activity.status !== "active";

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

        <p className="mt-1.5 text-xs font-semibold text-[#6355de] flex items-center gap-1.5">
          <Calendar className="w-3.5 h-3.5 text-[#6355de] shrink-0" />
          <span>{formattedDate}</span>
        </p>

        {activity.creatorName && (
          <p className="mt-1 text-xs text-slate-500">
            Por <span className="font-semibold text-slate-700">{activity.creatorName}</span>
          </p>
        )}

        {/* Plazas / Cupos e Insignia de Estado */}
        <div className="mt-3 flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5 text-slate-600 font-medium">
            <Users className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span>
              {activity.capacity} {activity.capacity === 1 ? "cupo disponible" : "cupos disponibles"}
            </span>
          </div>

          {showStatusBadge && statusBadge && (
            <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${statusBadge.className}`}>
              {statusBadge.label}
            </span>
          )}
        </div>
      </div>
    </article>
  );
}

import { CalendarX } from "lucide-react";
import type { ActivityListItem, ActivityScope } from "@/features/activities/domain/entities/activity.entity";
import { ActivityCard } from "./activity-card";

type ActivitiesFeedProps = {
  activities: ActivityListItem[];
  scope?: ActivityScope;
  emptyTitle?: string;
  emptyMessage?: string;
};

export function ActivitiesFeed({
  activities,
  scope,
  emptyTitle,
  emptyMessage,
}: ActivitiesFeedProps) {
  if (activities.length === 0) {
    const isMine = scope === "mine";
    const defaultTitle = isMine
      ? "Aún no has creado actividades"
      : "No hay actividades comunitarias";
    const defaultMessage = isMine
      ? "Toca el botón '+ Crear actividad' para publicar tu primera iniciativa solidaria."
      : "Actualmente no hay convocatorias de otros miembros disponibles.";

    return (
      <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
        <div className="w-16 h-16 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center mb-3">
          <CalendarX className="w-8 h-8" />
        </div>
        <h3 className="text-lg font-bold text-zinc-800">
          {emptyTitle || defaultTitle}
        </h3>
        <p className="text-sm text-zinc-500 mt-1 max-w-xs leading-relaxed">
          {emptyMessage || defaultMessage}
        </p>
      </div>
    );
  }

  return (
    <div className="pt-2" data-purpose="activities-feed">
      {activities.map((activity) => (
        <ActivityCard key={activity.id} activity={activity} />
      ))}
    </div>
  );
}

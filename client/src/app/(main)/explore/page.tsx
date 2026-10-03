import { Suspense } from "react";
import { getActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";
import { ActivitiesSkeleton } from "@/features/activities/presentation/components/elements/activities-skeleton";

async function ExploreListContent() {
  let activities = null;
  let hasError = false;

  try {
    activities = await getActivitiesQuery("others");
  } catch {
    hasError = true;
  }

  if (hasError || !activities) {
    return (
      <div className="py-12 px-4 text-center">
        <p className="text-sm text-red-500 font-medium">
          No se pudieron cargar las actividades en este momento. Intenta recargar la página.
        </p>
      </div>
    );
  }

  return (
    <ActivitiesFeed
      activities={activities}
      scope="others"
      emptyTitle="No hay actividades comunitarias"
      emptyMessage="Actualmente no hay convocatorias de otros miembros disponibles para explorar."
    />
  );
}

export default function ExplorePage() {
  return (
    <Suspense fallback={<ActivitiesSkeleton />}>
      <ExploreListContent />
    </Suspense>
  );
}

import { Suspense } from "react";
import { getActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";
import { ActivitiesSkeleton } from "@/features/activities/presentation/components/elements/activities-skeleton";
import { CreateActivitySheet } from "@/features/activities/presentation/components/dialogs/create-activity-sheet";

async function MyActivitiesListContent() {
  let activities = null;
  let hasError = false;

  try {
    activities = await getActivitiesQuery("mine");
  } catch {
    hasError = true;
  }

  if (hasError || !activities) {
    return (
      <div className="py-12 px-4 text-center">
        <p className="text-sm text-red-500 font-medium">
          No se pudieron cargar tus actividades en este momento. Intenta recargar la página.
        </p>
      </div>
    );
  }

  return (
    <ActivitiesFeed
      activities={activities}
      scope="mine"
      emptyTitle="Aún no has creado actividades"
      emptyMessage="Toca el botón '+ Crear actividad' para publicar tu primera iniciativa solidaria."
    />
  );
}

export default function MyActivitiesPage() {
  return (
    <>
      <Suspense fallback={<ActivitiesSkeleton />}>
        <MyActivitiesListContent />
      </Suspense>

      {/* Floating Action Button exclusivo de Mis Actividades */}
      <CreateActivitySheet />
    </>
  );
}

import { Suspense } from "react";
import { getActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";
import { ActivitiesSkeleton } from "@/features/activities/presentation/components/elements/activities-skeleton";
import { CreateActivitySheet } from "@/features/activities/presentation/components/dialogs/create-activity-sheet";

export const dynamic = "force-dynamic";


async function MyActivitiesListContent() {
  const activities = await getActivitiesQuery("mine");

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

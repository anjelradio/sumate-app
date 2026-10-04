import { Suspense } from "react";
import { getActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";
import { ActivitiesSkeleton } from "@/features/activities/presentation/components/elements/activities-skeleton";

export const dynamic = "force-dynamic";

async function ExploreListContent() {
  const activities = await getActivitiesQuery("others");

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

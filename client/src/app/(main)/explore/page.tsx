import { getExploreActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";

export const dynamic = "force-dynamic";

export default async function ExplorePage() {
  const activities = await getExploreActivitiesQuery();

  return (
    <ActivitiesFeed
      activities={activities}
      scope="others"
      emptyTitle="No hay actividades comunitarias"
      emptyMessage="Actualmente no hay convocatorias de otros miembros disponibles para explorar."
    />
  );
}

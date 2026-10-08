import { getMyActivitiesQuery } from "@/features/activities/presentation/queries/activity.query";
import { ActivitiesFeed } from "@/features/activities/presentation/components/elements/activities-feed";
import { CreateActivitySheet } from "@/features/activities/presentation/components/dialogs/create-activity-sheet";

export const dynamic = "force-dynamic";

export default async function MyActivitiesPage() {
  const activities = await getMyActivitiesQuery();

  return (
    <>
      <ActivitiesFeed
        activities={activities}
        scope="mine"
        emptyTitle="Aún no has creado actividades"
        emptyMessage="Toca el botón '+ Crear actividad' para publicar tu primera iniciativa solidaria."
      />
      <CreateActivitySheet />
    </>
  );
}

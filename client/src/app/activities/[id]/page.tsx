import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ActivityDetailView } from "@/features/activities/presentation/components/views/activity-detail-view";
import { getActivityDetailQuery } from "@/features/activities/presentation/queries/activity.query";

export const dynamic = "force-dynamic";

type PageProps = {
  params: Promise<{ id: string }>;
};

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { id } = await params;
  const activity = await getActivityDetailQuery(id);

  if (!activity) {
    return {
      title: "Actividad no encontrada - Súmate",
    };
  }

  return {
    title: `${activity.name} - Súmate`,
    description:
      activity.detail?.description ||
      `Conoce los detalles de ${activity.name} en Súmate y únete como voluntario.`,
  };
}

export default async function ActivityDetailPage({ params }: PageProps) {
  const { id } = await params;
  const activity = await getActivityDetailQuery(id);

  if (!activity) {
    notFound();
  }

  return <ActivityDetailView activity={activity} />;
}

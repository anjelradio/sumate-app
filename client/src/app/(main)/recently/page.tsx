import { getMyParticipationsQuery } from "@/features/participations/presentation/queries/participation.query";
import { RecentlyFeed } from "@/features/participations/presentation/components/elements/recently-feed";

export const dynamic = "force-dynamic";

export default async function RecentlyPage() {
  const participations = await getMyParticipationsQuery();

  return <RecentlyFeed participations={participations} />;
}

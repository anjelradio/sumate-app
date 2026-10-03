import { Suspense } from "react";
import { AppHeader } from "@/features/shared/presentation/components/layout/app-header";
import type { EventScope } from "@/features/events/domain/entities/event.entity";
import { getEventsQuery } from "@/features/events/presentation/queries/event.query";
import { EventsFeed } from "@/features/events/presentation/components/elements/events-feed";
import { EventsSegmentedNav } from "@/features/events/presentation/components/elements/events-segmented-nav";
import { EventsSkeleton } from "@/features/events/presentation/components/elements/events-skeleton";
import { CreateEventSheet } from "@/features/events/presentation/components/dialogs/create-event-sheet";

type HomePageProps = {
  searchParams?: Promise<{ scope?: string }>;
};

async function EventsListContent({ scope }: { scope: EventScope }) {
  try {
    const events = await getEventsQuery(scope);
    return <EventsFeed events={events} scope={scope} />;
  } catch (err) {
    return (
      <div className="py-12 px-4 text-center">
        <p className="text-sm text-red-500 font-medium">
          No se pudieron cargar los eventos en este momento. Intenta recargar la página.
        </p>
      </div>
    );
  }
}

export default async function HomePage({ searchParams }: HomePageProps) {
  const resolvedParams = searchParams ? await searchParams : undefined;
  const scope: EventScope = resolvedParams?.scope === "others" ? "others" : "mine";

  return (
    <div className="min-h-screen bg-[#f8f7fc] text-slate-800 flex flex-col selection:bg-[#ece9fc] selection:text-[#4334b8]">
      <AppHeader />

      <main className="w-full max-w-md mx-auto px-5 pt-3 pb-24 flex-1 flex flex-col">
        {/* Selector de pestañas segmentadas */}
        <EventsSegmentedNav activeScope={scope} />

        {/* Feed de eventos con Skeleton durante la carga */}
        <Suspense fallback={<EventsSkeleton />}>
          <EventsListContent scope={scope} />
        </Suspense>
      </main>

      {/* El botón flotante y bottom sheet solo se muestran en "Mis eventos" */}
      {scope === "mine" && <CreateEventSheet />}
    </div>
  );
}

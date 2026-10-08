"use client";

import { useEffect } from "react";
import type { ActivityDetailData } from "@/features/activities/domain/entities/activity.entity";
import { useActivityDetailUiStore } from "../../stores/activity-detail-ui.store";
import { LocationMapSheet } from "../dialogs/location-map-sheet";
import { ActivityDetailActions } from "../elements/activity-detail-actions";
import { ActivityDetailDescription } from "../elements/activity-detail-description";
import { ActivityDetailHeader } from "../elements/activity-detail-header";
import { ActivityDetailHero } from "../elements/activity-detail-hero";
import { ActivityDetailInfo } from "../elements/activity-detail-info";
import { ActivityDetailOrganizer } from "../elements/activity-detail-organizer";
import { ActivityDetailParticipants } from "../elements/activity-detail-participants";

type ActivityDetailViewProps = {
  activity: ActivityDetailData;
};

export function ActivityDetailView({ activity }: ActivityDetailViewProps) {
  const { isLocationSheetOpen, closeLocationSheet, reset } =
    useActivityDetailUiStore();

  useEffect(() => {
    return () => {
      reset();
    };
  }, [reset]);

  return (
    <div className="min-h-screen bg-white text-slate-900 flex flex-col justify-between selection:bg-indigo-100">
      <main className="w-full max-w-md mx-auto flex-1 pb-28 px-5 pt-2 sm:pt-4">
        {/* Cabecera superior con volver atrás, compartir y toggle de edición */}
        <ActivityDetailHeader activity={activity} />

        {/* Foto de portada y badge de estado */}
        <ActivityDetailHero activity={activity} />

        {/* Título, Fecha y Hora, Cupos y Ubicación */}
        <ActivityDetailInfo activity={activity} />

        {/* Descripción de la actividad */}
        <ActivityDetailDescription activity={activity} />

        {/* Sección del organizador */}
        <ActivityDetailOrganizer activity={activity} />

        {/* Participantes confirmados */}
        <ActivityDetailParticipants activity={activity} />
      </main>

      {/* Botón flotante de acción (Asistiré / Publicar / Cerrar convocatoria) */}
      <ActivityDetailActions activity={activity} />

      {/* Bottom Sheet con mapa Leaflet para edición de ubicación */}
      <LocationMapSheet
        activity={activity}
        isOpen={isLocationSheetOpen}
        onClose={closeLocationSheet}
      />
    </div>
  );
}

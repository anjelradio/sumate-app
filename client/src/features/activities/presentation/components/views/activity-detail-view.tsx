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

  const hasLocation = Boolean(
    activity.detail?.latitude != null && activity.detail?.longitude != null
  );
  const hasDescription = Boolean(activity.detail?.description?.trim());

  return (
    <div className="min-h-screen bg-white text-slate-900 flex flex-col justify-between selection:bg-indigo-100">
      <main className="w-full max-w-md mx-auto flex-1 pb-28 px-5 pt-2 sm:pt-4">
        {/* Cabecera superior con volver atrás, compartir y toggle de edición */}
        <ActivityDetailHeader
          activityName={activity.name}
          isOwner={activity.isOwner}
        />

        {/* Foto de portada y badge de estado */}
        <ActivityDetailHero
          activityId={activity.id}
          imageUrl={activity.imageUrl}
          activityName={activity.name}
          status={activity.status}
          isOwner={activity.isOwner}
        />

        {/* Título, Fecha y Hora, Cupos y Ubicación */}
        <ActivityDetailInfo
          activityId={activity.id}
          name={activity.name}
          date={activity.date}
          capacity={activity.capacity}
          isOwner={activity.isOwner}
          detail={activity.detail}
        />

        {/* Descripción de la actividad */}
        <ActivityDetailDescription
          activityId={activity.id}
          description={activity.detail?.description ?? null}
          isOwner={activity.isOwner}
        />

        {/* Sección del organizador */}
        <ActivityDetailOrganizer
          creatorName={activity.creatorName}
          creatorImage={activity.creatorImage}
        />
      </main>

      {/* Botón flotante de acción (Asistiré / Publicar / Cerrar convocatoria) */}
      <ActivityDetailActions
        activityId={activity.id}
        status={activity.status}
        isOwner={activity.isOwner}
        hasLocation={hasLocation}
        hasDescription={hasDescription}
      />

      {/* Bottom Sheet con mapa Leaflet para edición de ubicación */}
      <LocationMapSheet
        isOpen={isLocationSheetOpen}
        onClose={closeLocationSheet}
        activityId={activity.id}
        initialLat={activity.detail?.latitude}
        initialLng={activity.detail?.longitude}
        initialPlace={activity.detail?.place}
      />
    </div>
  );
}

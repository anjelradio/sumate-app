"use client";

import { useState, useTransition } from "react";
import { Check, CheckCircle2, Loader2, Lock, Rocket } from "lucide-react";
import type { ActivityStatus } from "@/features/activities/domain/entities/activity.entity";
import { appToast } from "@/features/shared/presentation/components/notifications/toast";
import {
  closeActivityAction,
  publishActivityAction,
} from "../../actions/activity.action";

type ActivityDetailActionsProps = {
  activityId: string;
  status: ActivityStatus;
  isOwner: boolean;
  hasLocation: boolean;
  hasDescription: boolean;
};

export function ActivityDetailActions({
  activityId,
  status,
  isOwner,
  hasLocation,
  hasDescription,
}: ActivityDetailActionsProps) {
  const [isPending, startTransition] = useTransition();
  const [hasJoined, setHasJoined] = useState(false);

  const handleVolunteerJoin = () => {
    if (hasJoined) {
      setHasJoined(false);
      appToast.info("Has cancelado tu confirmación de asistencia.");
    } else {
      setHasJoined(true);
      appToast.success("¡Excelente! Has confirmado tu asistencia a la actividad.");
    }
  };

  const handlePublish = () => {
    if (!hasLocation || !hasDescription) {
      const missing = [];
      if (!hasLocation) missing.push("ubicación en el mapa");
      if (!hasDescription) missing.push("descripción");
      appToast.error(
        "Requisitos incompletos",
        `Para publicar la actividad debes registrar: ${missing.join(" y ")}.`
      );
      return;
    }

    startTransition(async () => {
      const res = await publishActivityAction(activityId);
      if (!res.ok) {
        appToast.error(
          "Error al publicar",
          res.errors?.[0] ?? "No se pudo publicar la actividad."
        );
        return;
      }
      appToast.success("¡Actividad publicada con éxito! Ya es visible para todos.");
    });
  };

  const handleClose = () => {
    startTransition(async () => {
      const res = await closeActivityAction(activityId);
      if (!res.ok) {
        appToast.error(
          "Error al cerrar",
          res.errors?.[0] ?? "No se pudo cerrar la convocatoria."
        );
        return;
      }
      appToast.success("Convocatoria cerrada exitosamente.");
    });
  };

  return (
    <div className="fixed bottom-6 right-5 z-40 pointer-events-none">
      {!isOwner ? (
        status === "active" ? (
          <button
            type="button"
            onClick={handleVolunteerJoin}
            aria-label="Confirmar asistencia al evento"
            className={`pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full font-semibold text-sm shadow-lg transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 cursor-pointer ${
              hasJoined
                ? "bg-emerald-600 text-white shadow-emerald-600/35 focus:ring-emerald-600"
                : "bg-[#6355de] text-white shadow-[#6355de]/35 focus:ring-[#6355de]"
            }`}
          >
            {hasJoined ? (
              <>
                <CheckCircle2 className="w-5 h-5 stroke-current" />
                <span>Asistiré (Confirmado)</span>
              </>
            ) : (
              <>
                <Check className="w-5 h-5 stroke-current" />
                <span>Asistiré</span>
              </>
            )}
          </button>
        ) : (
          <button
            type="button"
            disabled
            className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-slate-300 text-slate-600 font-semibold text-sm cursor-not-allowed shadow-sm"
          >
            <Lock className="w-4 h-4" />
            <span>Convocatoria cerrada</span>
          </button>
        )
      ) : status === "draft" ? (
        <button
          type="button"
          onClick={handlePublish}
          disabled={isPending}
          aria-label="Publicar actividad"
          className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-[#6355de] text-white shadow-lg shadow-[#6355de]/35 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#6355de] font-semibold text-sm disabled:opacity-50 cursor-pointer"
        >
          {isPending ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Publicando...</span>
            </>
          ) : (
            <>
              <Rocket className="w-4 h-4" />
              <span>Publicar actividad</span>
            </>
          )}
        </button>
      ) : status === "active" ? (
        <button
          type="button"
          onClick={handleClose}
          disabled={isPending}
          aria-label="Cerrar convocatoria"
          className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-rose-600 text-white shadow-lg shadow-rose-600/35 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-600 font-semibold text-sm disabled:opacity-50 cursor-pointer"
        >
          {isPending ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Cerrando...</span>
            </>
          ) : (
            <>
              <Lock className="w-4 h-4" />
              <span>Cerrar convocatoria</span>
            </>
          )}
        </button>
      ) : (
        <button
          type="button"
          disabled
          className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-slate-300 text-slate-600 font-semibold text-sm cursor-not-allowed shadow-sm"
        >
          <Lock className="w-4 h-4" />
          <span>Convocatoria cerrada</span>
        </button>
      )}
    </div>
  );
}

"use client";

import { useState, useTransition } from "react";
import { Check, CheckCircle2, Loader2, Lock, Rocket } from "lucide-react";
import type { ActivityDetailData } from "@/features/activities/domain/entities/activity.entity";
import { appToast } from "@/features/shared/presentation/components/notifications/toast";
import {
  closeActivityAction,
  publishActivityAction,
} from "../../actions/activity.action";
import {
  joinActivityAction,
  leaveActivityAction,
} from "@/features/participations/presentation/actions/participation.action";
import { ConfirmJoinDialog } from "@/features/participations/presentation/components/dialogs/confirm-join-dialog";
import { ConfirmLeaveDialog } from "@/features/participations/presentation/components/dialogs/confirm-leave-dialog";

type ActivityDetailActionsProps = {
  activity: ActivityDetailData;
};

export function ActivityDetailActions({
  activity,
}: ActivityDetailActionsProps) {
  const { id: activityId, name: activityName, status, isOwner, isParticipating, detail } = activity;
  const hasLocation = Boolean(
    detail?.latitude != null && detail?.longitude != null
  );
  const hasDescription = Boolean(detail?.description?.trim());
  const isPast = Boolean(
    activity.date && new Date(activity.date).getTime() <= Date.now()
  );
  const isFull = (activity.participants?.length ?? 0) >= activity.capacity;
  const [isPending, startTransition] = useTransition();
  const [joinDialogOpen, setJoinDialogOpen] = useState(false);
  const [leaveDialogOpen, setLeaveDialogOpen] = useState(false);

  const handleConfirmJoin = () => {
    startTransition(async () => {
      const res = await joinActivityAction(activityId);
      if (!res.ok) {
        appToast.error(
          "Error al unirse a la actividad",
          res.errors?.[0] ?? "No se pudo registrar tu participación."
        );
        return;
      }
      setJoinDialogOpen(false);
      appToast.success("¡Excelente! Has confirmado tu asistencia a la actividad.");
    });
  };

  const handleConfirmLeave = () => {
    startTransition(async () => {
      const res = await leaveActivityAction(activityId);
      if (!res.ok) {
        appToast.error(
          "Error al cancelar participación",
          res.errors?.[0] ?? "No se pudo cancelar tu participación."
        );
        return;
      }
      setLeaveDialogOpen(false);
      appToast.success("Has cancelado tu confirmación de asistencia.");
    });
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
    <>
      <div className="fixed bottom-6 right-5 z-40 pointer-events-none">
        {!isOwner ? (
          isPast ? (
            isParticipating ? (
              <button
                type="button"
                disabled
                className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-slate-300 text-slate-600 font-semibold text-sm cursor-not-allowed shadow-sm"
              >
                <CheckCircle2 className="w-5 h-5 stroke-current" />
                <span>Asististe</span>
              </button>
            ) : (
              <button
                type="button"
                disabled
                className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-slate-300 text-slate-600 font-semibold text-sm cursor-not-allowed shadow-sm"
              >
                <Lock className="w-4 h-4" />
                <span>Actividad finalizada</span>
              </button>
            )
          ) : status === "active" ? (
            isParticipating ? (
              <button
                type="button"
                onClick={() => setLeaveDialogOpen(true)}
                disabled={isPending}
                aria-label="Cancelar participación en el evento"
                className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full font-semibold text-sm shadow-lg shadow-emerald-600/35 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-600 cursor-pointer bg-emerald-600 hover:bg-emerald-700 text-white"
              >
                <CheckCircle2 className="w-5 h-5 stroke-current" />
                <span>Asistiré (Confirmado)</span>
              </button>
            ) : isFull ? (
              <button
                type="button"
                disabled
                className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-slate-300 text-slate-600 font-semibold text-sm cursor-not-allowed shadow-sm"
              >
                <Lock className="w-4 h-4" />
                <span>Cupos agotados</span>
              </button>
            ) : (
              <button
                type="button"
                onClick={() => setJoinDialogOpen(true)}
                disabled={isPending}
                aria-label="Confirmar asistencia al evento"
                className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full font-semibold text-sm shadow-lg shadow-[#6355de]/35 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#6355de] cursor-pointer bg-[#6355de] hover:bg-[#5244cc] text-white"
              >
                <Check className="w-5 h-5 stroke-current" />
                <span>Participar</span>
              </button>
            )
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

      <ConfirmJoinDialog
        isOpen={joinDialogOpen}
        onOpenChange={setJoinDialogOpen}
        onConfirm={handleConfirmJoin}
        isPending={isPending}
        activityName={activityName}
      />
      <ConfirmLeaveDialog
        isOpen={leaveDialogOpen}
        onOpenChange={setLeaveDialogOpen}
        onConfirm={handleConfirmLeave}
        isPending={isPending}
        activityName={activityName}
      />
    </>
  );
}

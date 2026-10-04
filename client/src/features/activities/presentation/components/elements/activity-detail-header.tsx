"use client";

import { useRouter } from "next/navigation";
import { ChevronLeft, Eye, Pencil, Share2 } from "lucide-react";
import { appToast } from "@/features/shared/presentation/components/notifications/toast";
import { useActivityDetailUiStore } from "../../stores/activity-detail-ui.store";

type ActivityDetailHeaderProps = {
  activityName: string;
  isOwner: boolean;
};

export function ActivityDetailHeader({
  activityName,
  isOwner,
}: ActivityDetailHeaderProps) {
  const router = useRouter();
  const { isEditMode, toggleEditMode } = useActivityDetailUiStore();

  const handleBack = () => {
    if (window.history.length > 1) {
      router.back();
    } else {
      router.push("/explore");
    }
  };

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({
          title: activityName,
          text: `Te invito a unirte a "${activityName}" en Súmate`,
          url,
        });
        return;
      } catch (err: any) {
        if (err.name === "AbortError") return;
      }
    }

    try {
      await navigator.clipboard.writeText(url);
      appToast.success("Enlace copiado al portapapeles.");
    } catch {
      appToast.info("Copia el enlace de la barra de direcciones.");
    }
  };

  return (
    <header
      className="sticky top-0 z-40 flex items-center justify-between py-3 mb-4 backdrop-blur-md bg-white/95 transition-colors"
      data-purpose="top-navigation-bar"
    >
      {/* Botón Volver Atrás */}
      <button
        type="button"
        onClick={handleBack}
        aria-label="Volver atrás"
        className="w-11 h-11 rounded-full bg-slate-100 flex items-center justify-center text-slate-700 active:scale-95 hover:bg-slate-200 transition-all cursor-pointer"
      >
        <ChevronLeft className="w-5 h-5 -ml-0.5" />
      </button>

      {/* Acciones de la derecha */}
      <div className="flex items-center space-x-2.5">
        <button
          type="button"
          onClick={handleShare}
          aria-label="Compartir evento"
          className="w-11 h-11 rounded-full bg-slate-100 flex items-center justify-center text-slate-700 active:scale-95 hover:bg-slate-200 transition-all cursor-pointer"
        >
          <Share2 className="w-5 h-5" />
        </button>

        {isOwner && (
          <button
            type="button"
            onClick={toggleEditMode}
            aria-label={isEditMode ? "Volver a modo lectura" : "Activar modo edición"}
            title={isEditMode ? "Volver a modo lectura" : "Editar actividad"}
            className={`w-11 h-11 rounded-full flex items-center justify-center active:scale-95 transition-all cursor-pointer ${
              isEditMode
                ? "bg-[#6355de] text-white shadow-md shadow-[#6355de]/30 ring-2 ring-[#6355de] ring-offset-2"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {isEditMode ? <Eye className="w-5 h-5" /> : <Pencil className="w-5 h-5" />}
          </button>
        )}
      </div>
    </header>
  );
}

"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { AppSheet } from "@/features/shared/presentation/components/dialogs/app-sheet";
import { CreateEventForm } from "../forms/create-event-form";

export function CreateEventSheet() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Botón flotante estilizado según design/events/events-home.html */}
      <div className="fixed bottom-6 right-5 z-50 max-w-md pointer-events-none">
        <button
          type="button"
          onClick={() => setOpen(true)}
          aria-label="Crear nuevo evento"
          className="pointer-events-auto flex items-center justify-center gap-2 px-5 py-3.5 rounded-full bg-[#6355de] text-white shadow-lg shadow-[#6355de]/35 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#6355de] font-semibold text-sm cursor-pointer"
        >
          <Plus className="w-5 h-5 stroke-[2.5]" />
          <span>Crear evento</span>
        </button>
      </div>

      {/* Diálogo inferior (Bottom Sheet) */}
      <AppSheet
        open={open}
        onOpenChange={setOpen}
        side="bottom"
        title="Crear nuevo evento"
        description="Completa la información básica para convocar a la comunidad de Súmate."
        height="auto"
        bodyClassName="p-5 max-h-[85vh] overflow-y-auto no-scrollbar"
      >
        <div className="pt-2 pb-4">
          <CreateEventForm onSuccess={() => setOpen(false)} />
        </div>
      </AppSheet>
    </>
  );
}

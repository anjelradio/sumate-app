"use client";

import { useState, useTransition, type FormEvent } from "react";
import { Check, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { appToast } from "@/features/shared/presentation/components/notifications/toast";
import { useSubmitWithSchema } from "@/features/shared/presentation/hooks/use-submit-with-schema";
import { updateActivityDescriptionAction } from "../../actions/activity.action";
import { EditDescriptionSchema } from "@/features/activities/infrastructure/schemas/activity.schemas";

type EditActivityDescriptionFormProps = {
  activityId: string;
  initialDescription: string | null;
  onCancel: () => void;
  onSuccess: () => void;
};

export function EditActivityDescriptionForm({
  activityId,
  initialDescription,
  onCancel,
  onSuccess,
}: EditActivityDescriptionFormProps) {
  const [descriptionText, setDescriptionText] = useState(initialDescription ?? "");
  const [isPending, startTransition] = useTransition();
  const submitWithSchema = useSubmitWithSchema();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    startTransition(async () => {
      await submitWithSchema({
        schema: EditDescriptionSchema,
        payload: { description: descriptionText },
        action: (data) =>
          updateActivityDescriptionAction(activityId, data.description),
        onSuccess: () => {
          appToast.success("Descripción actualizada.");
          onSuccess();
        },
        errorTitle: "Error al actualizar descripción",
      });
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <textarea
        rows={5}
        value={descriptionText}
        onChange={(e) => setDescriptionText(e.target.value)}
        className="w-full text-sm leading-relaxed text-slate-700 border border-slate-300 rounded-xl p-3 focus:ring-2 focus:ring-[#6355de] focus:outline-none"
        placeholder="Describe la actividad, requisitos para voluntarios y objetivo social..."
        autoFocus
      />
      <div className="grid grid-cols-2 gap-3 w-full pt-1">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isPending}
          className="w-full rounded-xl cursor-pointer"
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          disabled={isPending}
          className="w-full bg-[#6355de] hover:bg-[#5446cc] text-white rounded-xl flex items-center justify-center gap-2 cursor-pointer"
        >
          {isPending ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Check className="w-4 h-4" />
          )}
          Guardar
        </Button>
      </div>
    </form>
  );
}

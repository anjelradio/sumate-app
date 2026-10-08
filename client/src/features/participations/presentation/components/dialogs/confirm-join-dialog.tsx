"use client";

import {
  AlertDialog,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { CheckCircle2 } from "lucide-react";

type ConfirmJoinDialogProps = {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void;
  isPending: boolean;
  activityName?: string;
};

export function ConfirmJoinDialog({
  isOpen,
  onOpenChange,
  onConfirm,
  isPending,
  activityName,
}: ConfirmJoinDialogProps) {
  return (
    <AlertDialog open={isOpen} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-400">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <AlertDialogTitle className="text-center">Confirmar asistencia</AlertDialogTitle>
          <AlertDialogDescription className="text-center">
            {activityName ? (
              <>
                ¿Deseas confirmar tu participación como voluntario en{" "}
                <span className="font-semibold text-foreground">&ldquo;{activityName}&rdquo;</span>?
                Al confirmar, se reservará tu plaza de inmediato.
              </>
            ) : (
              "¿Deseas confirmar tu participación como voluntario en esta actividad? Al confirmar, se reservará tu plaza de inmediato."
            )}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter className="sm:justify-center">
          <AlertDialogCancel disabled={isPending}>Cancelar</AlertDialogCancel>
          <Button
            type="button"
            disabled={isPending}
            onClick={onConfirm}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold cursor-pointer"
          >
            {isPending ? (
              <>
                <Spinner className="size-4 mr-2" />
                <span>Confirmando...</span>
              </>
            ) : (
              "Confirmar asistencia"
            )}
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

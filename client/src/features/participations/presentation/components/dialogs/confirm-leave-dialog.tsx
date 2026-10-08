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
import { AlertCircle } from "lucide-react";

type ConfirmLeaveDialogProps = {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void;
  isPending: boolean;
  activityName?: string;
};

export function ConfirmLeaveDialog({
  isOpen,
  onOpenChange,
  onConfirm,
  isPending,
  activityName,
}: ConfirmLeaveDialogProps) {
  return (
    <AlertDialog open={isOpen} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-rose-100 text-rose-600 dark:bg-rose-950 dark:text-rose-400">
            <AlertCircle className="h-6 w-6" />
          </div>
          <AlertDialogTitle className="text-center">Cancelar participación</AlertDialogTitle>
          <AlertDialogDescription className="text-center">
            {activityName ? (
              <>
                ¿Estás seguro de que deseas cancelar tu participación en{" "}
                <span className="font-semibold text-foreground">&ldquo;{activityName}&rdquo;</span>?
                Tu cupo reservado quedará disponible para que otro voluntario pueda unirse.
              </>
            ) : (
              "¿Estás seguro de que deseas cancelar tu participación? Tu cupo reservado quedará disponible para que otro voluntario pueda unirse."
            )}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter className="sm:justify-center">
          <AlertDialogCancel disabled={isPending}>Mantener mi lugar</AlertDialogCancel>
          <Button
            type="button"
            variant="destructive"
            disabled={isPending}
            onClick={onConfirm}
            className="cursor-pointer"
          >
            {isPending ? (
              <>
                <Spinner className="size-4 mr-2" />
                <span>Cancelando...</span>
              </>
            ) : (
              "Sí, cancelar participación"
            )}
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

"use client";

import type { ReactNode } from "react";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

export type AppSheetSize = "sm" | "md" | "lg" | "xl" | "full" | "auto";
export type AppSheetSide = "top" | "bottom" | "left" | "right";

export type AppSheetProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title?: string;
  description?: string;
  children: ReactNode;
  side?: AppSheetSide;
  width?: AppSheetSize;
  height?: AppSheetSize;
  className?: string;
  bodyClassName?: string;
  preventCloseOnOutsideClick?: boolean;
  showCloseButton?: boolean;
  showDivider?: boolean;
  autoFocusInput?: boolean;
  showHeader?: boolean;
};

export function AppSheet({
  open,
  onOpenChange,
  title,
  description,
  children,
  side = "right",
  width,
  height,
  className,
  bodyClassName,
  preventCloseOnOutsideClick = false,
  showCloseButton = false,
  showDivider = false,
  autoFocusInput = false,
  showHeader = true,
}: AppSheetProps) {
  // Computamos las clases dinámicas para controlar ancho y alto independientemente
  const getDimensionsClass = () => {
    // 1. Resolver Ancho
    const resolvedWidth = width || (side === "left" || side === "right" ? "md" : "full");
    const baseWidth = {
      sm: "w-full sm:max-w-sm",
      md: "w-full sm:max-w-md",
      lg: "w-full sm:max-w-lg",
      xl: "w-full sm:max-w-xl",
      full: "w-full sm:max-w-full",
      auto: "w-auto",
    }[resolvedWidth];

    // Si viene de arriba/abajo y tiene un ancho restringido, lo centramos horizontalmente
    const centerHorizontally = (side === "top" || side === "bottom") && resolvedWidth !== "full" ? "mx-auto" : "";

    // 2. Resolver Alto
    const resolvedHeight = height || (side === "top" || side === "bottom" ? "auto" : "full");
    const baseHeight = {
      sm: "h-full max-h-[33vh]",
      md: "h-full max-h-[50vh]",
      lg: "h-full max-h-[75vh]",
      xl: "h-full max-h-[90vh]",
      full: "h-full max-h-screen",
      auto: "h-auto",
    }[resolvedHeight];

    // Si viene de izquierda/derecha y tiene un alto restringido, lo centramos verticalmente
    const centerVertically = (side === "left" || side === "right") && resolvedHeight !== "full" ? "my-auto" : "";

    return cn(baseWidth, centerHorizontally, baseHeight, centerVertically);
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side={side}
        showCloseButton={showCloseButton}
        onOpenAutoFocus={
          autoFocusInput ? undefined : (e) => e.preventDefault()
        }
        // Configuración para evitar cierre al hacer clic afuera (similar al Modal)
        onPointerDownOutside={
          preventCloseOnOutsideClick ? (e) => e.preventDefault() : undefined
        }
        onInteractOutside={
          preventCloseOnOutsideClick ? (e) => e.preventDefault() : undefined
        }
        className={cn(
          "flex flex-col bg-white p-0 text-popover-foreground shadow-2xl",
          getDimensionsClass(),
          side === "top" && "rounded-b-3xl",
          side === "bottom" && "rounded-t-3xl",
          className
        )}
      >
        {/* Handle pill para bottom sheet */}
        {side === "bottom" && (
          <div className="w-10 h-1 bg-slate-200 rounded-full mx-auto mt-3 mb-1 shrink-0" />
        )}

        {showHeader && title ? (
          <div
            className={cn(
              "px-5 pt-2 pb-1",
              showDivider && "border-b border-slate-100 pb-2"
            )}
          >
            <SheetHeader className="p-0 space-y-0.5 text-left">
              <SheetTitle className="text-base font-bold text-slate-900 tracking-tight">
                {title}
              </SheetTitle>
              {description ? (
                <SheetDescription className="text-xs text-slate-500 font-medium">
                  {description}
                </SheetDescription>
              ) : null}
            </SheetHeader>
          </div>
        ) : (
          <SheetHeader className="sr-only">
            <SheetTitle>{title || "Diálogo"}</SheetTitle>
            {description ? <SheetDescription>{description}</SheetDescription> : null}
          </SheetHeader>
        )}
        
        {/* Cuerpo del sheet con scroll interno si hay mucho contenido */}
        <div className={cn("px-6 py-4 flex-1 overflow-y-auto", bodyClassName)}>
          {children}
        </div>
      </SheetContent>
    </Sheet>
  );
}

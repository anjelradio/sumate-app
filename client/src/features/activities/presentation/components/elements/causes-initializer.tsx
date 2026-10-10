"use client";

import { useEffect, useRef } from "react";
import type { Cause } from "@/features/activities/domain/entities/activity.entity";
import { useCausesStore } from "../../stores/causes.store";

type CausesInitializerProps = {
  initialCauses: Cause[];
};

export function CausesInitializer({ initialCauses }: CausesInitializerProps) {
  const initialized = useRef(false);

  if (!initialized.current && initialCauses && initialCauses.length > 0) {
    useCausesStore.getState().setCauses(initialCauses);
    initialized.current = true;
  }

  useEffect(() => {
    if (initialCauses && initialCauses.length > 0) {
      useCausesStore.getState().setCauses(initialCauses);
    }
  }, [initialCauses]);

  return null;
}

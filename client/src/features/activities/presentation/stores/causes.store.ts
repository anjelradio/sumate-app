import { create } from "zustand";
import type { Cause } from "@/features/activities/domain/entities/activity.entity";
import { activityRepositoryImpl } from "@/features/activities/infrastructure/repositories/activity.repository";

interface CausesStoreState {
  causes: Cause[];
  isLoaded: boolean;
  isLoading: boolean;
  setCauses: (causes: Cause[]) => void;
  fetchCauses: () => Promise<Cause[]>;
}

export const useCausesStore = create<CausesStoreState>((set, get) => ({
  causes: [],
  isLoaded: false,
  isLoading: false,

  setCauses: (causes: Cause[]) =>
    set({
      causes,
      isLoaded: causes.length > 0,
      isLoading: false,
    }),

  fetchCauses: async (): Promise<Cause[]> => {
    const { causes, isLoaded, isLoading } = get();
    if (isLoaded && causes.length > 0) {
      return causes;
    }
    if (isLoading) {
      return causes;
    }

    set({ isLoading: true });
    try {
      const res = await activityRepositoryImpl.listCauses();
      if (res.ok && res.data) {
        set({ causes: res.data, isLoaded: true, isLoading: false });
        return res.data;
      }
    } catch {
      // Retener estado previo en caso de fallo
    } finally {
      set({ isLoading: false });
    }
    return get().causes;
  },
}));

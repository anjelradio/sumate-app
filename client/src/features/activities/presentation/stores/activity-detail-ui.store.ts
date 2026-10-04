import { create } from "zustand";

export type EditableField =
  | "image"
  | "title"
  | "date"
  | "capacity"
  | "location"
  | "description";

interface ActivityDetailUiState {
  isEditMode: boolean;
  activeField: EditableField | null;
  isLocationSheetOpen: boolean;
  toggleEditMode: () => void;
  setEditMode: (enabled: boolean) => void;
  setActiveField: (field: EditableField | null) => void;
  openLocationSheet: () => void;
  closeLocationSheet: () => void;
  reset: () => void;
}

export const useActivityDetailUiStore = create<ActivityDetailUiState>((set) => ({
  isEditMode: false,
  activeField: null,
  isLocationSheetOpen: false,

  toggleEditMode: () =>
    set((state) => ({
      isEditMode: !state.isEditMode,
      activeField: null,
      isLocationSheetOpen: false,
    })),

  setEditMode: (enabled: boolean) =>
    set({
      isEditMode: enabled,
      activeField: null,
      isLocationSheetOpen: false,
    }),

  setActiveField: (field: EditableField | null) =>
    set({ activeField: field }),

  openLocationSheet: () =>
    set({ isLocationSheetOpen: true, activeField: "location" }),

  closeLocationSheet: () =>
    set({ isLocationSheetOpen: false, activeField: null }),

  reset: () =>
    set({
      isEditMode: false,
      activeField: null,
      isLocationSheetOpen: false,
    }),
}));

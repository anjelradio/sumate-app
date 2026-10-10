"use client";

import { useCallback, useMemo, useState } from "react";
import type {
  ActivityListItem,
  CapacityRangeFilter,
  DatePresetFilter,
  SearchFilterState,
  TimeOfDayFilter,
} from "../../domain/entities/activity.entity";
import { activityRepositoryImpl } from "../../infrastructure/repositories/activity.repository";

export const DEFAULT_SEARCH_FILTERS: SearchFilterState = {
  timeOfDay: "any",
  datePreset: "upcoming",
  capacityRange: "any",
  causeIds: [],
};

export function useActivitySearch() {
  const [query, setQuery] = useState<string>("");
  const [filters, setFilters] = useState<SearchFilterState>(DEFAULT_SEARCH_FILTERS);
  const [draftFilters, setDraftFilters] = useState<SearchFilterState>(DEFAULT_SEARCH_FILTERS);
  const [isFiltersSheetOpen, setIsFiltersSheetOpen] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [items, setItems] = useState<ActivityListItem[]>([]);

  const activeFiltersCount = useMemo(() => {
    let count = 0;
    if (filters.timeOfDay !== "any") count++;
    if (filters.datePreset !== "upcoming") count++;
    if (filters.capacityRange !== "any") count++;
    if (filters.causeIds.length > 0) count += filters.causeIds.length;
    return count;
  }, [filters]);

  const hasActiveFilters = activeFiltersCount > 0;

  const executeSearch = useCallback(
    async (queryToSearch: string, filtersToSearch: SearchFilterState) => {
      const trimmedQuery = queryToSearch.trim();
      const areFiltersDefault =
        filtersToSearch.timeOfDay === "any" &&
        filtersToSearch.datePreset === "upcoming" &&
        filtersToSearch.capacityRange === "any" &&
        filtersToSearch.causeIds.length === 0;

      // Si no hay texto y los filtros están en valores por defecto, resetear a vista inicial
      if (!trimmedQuery && areFiltersDefault) {
        setHasSearched(false);
        setItems([]);
        setIsLoading(false);
        return;
      }

      setHasSearched(true);
      setIsLoading(true);

      try {
        const res = await activityRepositoryImpl.searchActivities({
          q: trimmedQuery || undefined,
          timeOfDay: filtersToSearch.timeOfDay,
          datePreset: filtersToSearch.datePreset,
          capacityRange: filtersToSearch.capacityRange,
          causeIds: filtersToSearch.causeIds,
        });

        if (res.ok) {
          setItems(res.data);
        } else {
          setItems([]);
        }
      } catch {
        setItems([]);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const submitSearch = () => {
    executeSearch(query, filters);
  };

  const openFiltersSheet = () => {
    setDraftFilters(filters);
    setIsFiltersSheetOpen(true);
  };

  const closeFiltersSheet = () => {
    setIsFiltersSheetOpen(false);
  };

  const applyDraftFilters = () => {
    setFilters(draftFilters);
    setIsFiltersSheetOpen(false);
    executeSearch(query, draftFilters);
  };

  const resetDraftFilters = () => {
    setDraftFilters(DEFAULT_SEARCH_FILTERS);
  };

  const clearQuery = () => {
    setQuery("");
    const areFiltersDefault =
      filters.timeOfDay === "any" &&
      filters.datePreset === "upcoming" &&
      filters.capacityRange === "any" &&
      filters.causeIds.length === 0;

    if (areFiltersDefault) {
      setHasSearched(false);
      setItems([]);
    } else {
      executeSearch("", filters);
    }
  };

  return {
    query,
    setQuery,
    clearQuery,
    submitSearch,
    filters,
    draftFilters,
    setDraftFilters,
    isFiltersSheetOpen,
    setIsFiltersSheetOpen,
    openFiltersSheet,
    closeFiltersSheet,
    applyDraftFilters,
    resetDraftFilters,
    hasSearched,
    isLoading,
    items,
    activeFiltersCount,
    hasActiveFilters,
  };
}
